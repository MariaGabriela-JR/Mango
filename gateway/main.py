from fastapi import FastAPI, HTTPException, Header, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import httpx
import aio_pika
import json
import os
import uuid
from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Gateway API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurações
RESTAPI_URL = os.getenv("RESTAPI_URL", "http://restapi:8000")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
QUEUE_NAME = os.getenv("QUEUE_NAME", "patients")

# Cache de conexão RabbitMQ
_rabbit_connection = None

async def get_rabbitmq_channel():
    global _rabbit_connection
    if _rabbit_connection is None or _rabbit_connection.is_closed:
        _rabbit_connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await _rabbit_connection.channel()
    await channel.declare_queue(QUEUE_NAME, durable=True)
    return channel

async def authenticate_token(token: str) -> dict:
    """Delega a autenticação para o REST API"""
    try:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            
            # O REST API valida o token e retorna os dados do cientista
            response = await client.get(
                f"{RESTAPI_URL}/restapi/scientists/profile/", 
                headers=headers,
                timeout=10.0
            )
            
            if response.status_code == 200:
                scientist_data = response.json()
                return {
                    "scientist_id": scientist_data.get("id"),
                    "email": scientist_data.get("email"),
                    "is_verified": scientist_data.get("is_verified", False)
                }
            else:
                # Se o REST API rejeitar o token
                print(f"REST API rejeitou token: {response.status_code} - {response.text}")
                raise HTTPException(status_code=401, detail="Token inválido")
                
    except httpx.RequestError as e:
        print(f"Erro de conexão com REST API: {e}")
        raise HTTPException(status_code=503, detail="Serviço de autenticação indisponível")

class PatientMetadata(BaseModel):
    """Metadados do paciente que vêm do frontend"""
    age: Optional[int] = None
    gender: Optional[str] = None
    clinical_notes: Optional[str] = None

class ProcessPatientRequest(BaseModel):
    first_name: str
    last_name: str
    cpf: str
    password: str
    birth_date: str
    gender: str
    is_test: bool = False
    patient_metadata: Optional[dict] = {}
    edf_file_data: Optional[dict] = None

class EDFFileRequest(BaseModel):
    patient_iid: str
    session_name: str
    file_path: str
    patient_metadata: PatientMetadata  # Metadados vêm do frontend
    additional_metadata: Optional[dict] = None

def prepare_fastapi_payload(enriched_data: dict) -> dict:
    """Prepara os dados no formato esperado pelo FastAPI - SEM PASSWORD"""
    
    if 'password' in enriched_data:
        del enriched_data['password']
    
    fastapi_payload = {
        "action": "process_patient_data",
        "scientist_data": {
            "scientist_id": enriched_data["scientist_id"],
            "email": enriched_data["scientist_metadata"]["email"],
            "is_verified": enriched_data["scientist_metadata"]["is_verified"]
        },
        "patient_data": {
            "patient_iid": enriched_data["patient_iid"],
            "session_name": enriched_data["session_name"],
            "file_path": enriched_data["file_path"],
            # Metadados do frontend
            "age": enriched_data["patient_metadata"].get("age"),
            "gender": enriched_data["patient_metadata"].get("gender"),
            "clinical_notes": enriched_data["patient_metadata"].get("clinical_notes", ""),
            "additional_metadata": enriched_data.get("additional_metadata", {})
        },
        "processing_context": {
            "received_at": datetime.utcnow().isoformat(),
            "processing_timestamp": enriched_data["processing_timestamp"]
        }
    }
    
    return fastapi_payload

async def publish_to_rabbitmq(enriched_data: dict):
    """Publica dados formatados para o FastAPI no RabbitMQ"""
    try:
        channel = await get_rabbitmq_channel()
        
        # Prepara dados no formato do FastAPI
        fastapi_payload = prepare_fastapi_payload(enriched_data)
        
        message_body = json.dumps(fastapi_payload).encode()
        
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=message_body,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                headers={
                    "patient_iid": enriched_data["patient_iid"],
                    "scientist_id": enriched_data["scientist_id"],
                    "session_name": enriched_data["session_name"],
                    "action": "process_patient_data"
                }
            ),
            routing_key=QUEUE_NAME
        )
        
        print(f"✅ Mensagem publicada no RabbitMQ para paciente {enriched_data['patient_iid']}")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao publicar mensagem: {str(e)}")

@app.post("/api/process-patient")
async def process_patient(
    request: ProcessPatientRequest,
    background_tasks: BackgroundTasks,
    authorization: Optional[str] = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token de autenticação necessário")
    
    token = authorization.replace("Bearer ", "")

    try:
        # 1. Autentica cientista via REST API
        auth_data = await authenticate_token(token)
        scientist_id = auth_data.get("scientist_id")
        
        if not auth_data.get("is_verified", False):
            raise HTTPException(status_code=403, detail="Cientista não verificado")

        # 2. Cria paciente no REST API
        async with httpx.AsyncClient() as client:
            patient_payload = {
                "first_name": request.first_name,
                "last_name": request.last_name,
                "cpf": request.cpf,
                "password": request.password,
                "birth_date": request.birth_date,
                "gender": request.gender,
                "is_test": request.is_test
            }
            
            create_resp = await client.post(
                f"{RESTAPI_URL}/restapi/patients/register/",
                json=patient_payload,
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if create_resp.status_code != 201:
                error_detail = create_resp.json().get("detail", "Erro ao criar paciente")
                raise HTTPException(status_code=create_resp.status_code, detail=error_detail)
            
            patient_data = create_resp.json()
            patient_iid = patient_data["patient_iid"]

        enriched_data = {
            "patient_iid": patient_iid,
            "scientist_id": scientist_id,
            "session_name": request.edf_file_data.get("session_name", "default_session") if request.edf_file_data else "default_session",
            "file_path": request.edf_file_data.get("file_path", "") if request.edf_file_data else "",
            "patient_metadata": request.patient_metadata.dict() if hasattr(request.patient_metadata, 'dict') else (request.patient_metadata or {}),
            "scientist_metadata": auth_data,
            "processing_timestamp": datetime.utcnow().isoformat()
        }

        # 4. Publica no RabbitMQ (SEM PASSWORD)
        background_tasks.add_task(publish_to_rabbitmq, enriched_data)

        return {
            "status": "success",
            "message": "Paciente criado e enviado para processamento",
            "patient_iid": patient_iid,
            "scientist_id": scientist_id,
            "timestamp": datetime.utcnow().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@app.post("/api/process-edf-file")
async def process_edf_file(
    request: EDFFileRequest,
    background_tasks: BackgroundTasks,
    authorization: Optional[str] = Header(None)
):
    """
    Processa arquivo EDF - fluxo simplificado
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token de autenticação necessário")
    
    token = authorization.replace("Bearer ", "")
    
    try:
        # Apenas autenticação
        auth_data = await authenticate_token(token)
        scientist_id = auth_data.get("scientist_id")
        
        # Preparar dados enriquecidos
        enriched_data = {
            "patient_iid": request.patient_iid,
            "scientist_id": scientist_id,
            "session_name": request.session_name,
            "file_path": request.file_path,
            "patient_metadata": request.patient_metadata.dict(),  # Do frontend
            "scientist_metadata": auth_data,  # Do REST API
            "processing_timestamp": datetime.utcnow().isoformat(),
            "additional_metadata": request.additional_metadata or {}
        }
        
        # Publicar no RabbitMQ
        background_tasks.add_task(publish_to_rabbitmq, enriched_data)
        
        return {
            "status": "processing",
            "patient_iid": request.patient_iid,
            "session_name": request.session_name,
            "file_path": request.file_path,
            "message": "Arquivo EDF enviado para processamento",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/api/available-patients")
async def get_available_patients(authorization: Optional[str] = Header(None)):
    """Endpoint mantido para compatibilidade (retorna lista vazia)"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token necessário")
    
    # Como os metadados agora vêm do frontend, retornamos lista vazia
    # ou pode remover este endpoint se não for mais necessário
    return {"patients": [], "message": "Metadados agora devem ser enviados via frontend"}

@app.get("/health")
async def health_check():
    """Health check simplificado"""
    # RabbitMQ
    try:
        channel = await get_rabbitmq_channel()
        rabbit_status = "connected"
        await channel.close()
    except Exception as e:
        rabbit_status = f"error: {str(e)}"
    
    # REST API - apenas testa se está respondendo
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{RESTAPI_URL}/restapi/admin/", timeout=5.0)
            restapi_status = "connected" if response.status_code < 500 else f"http_{response.status_code}"
    except Exception as e:
        restapi_status = f"error: {str(e)}"
    
    return {
        "status": "healthy", 
        "service": "gateway",
        "dependencies": {
            "rabbitmq": rabbit_status,
            "restapi": restapi_status
        }
    }

@app.on_event("startup")
async def startup_event():
    """Inicializa conexão RabbitMQ"""
    try:
        await get_rabbitmq_channel()
        print("✅ Gateway conectado ao RabbitMQ")
    except Exception as e:
        print(f"❌ Erro ao conectar com RabbitMQ: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Fecha conexões"""
    global _rabbit_connection
    if _rabbit_connection:
        await _rabbit_connection.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)