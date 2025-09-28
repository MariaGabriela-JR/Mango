from fastapi import APIRouter, HTTPException, Header, BackgroundTasks, Query
from pydantic import BaseModel
from typing import Optional
import httpx
import aio_pika
import json
from datetime import datetime
import os

# Configurações
RESTAPI_URL = os.getenv("RESTAPI_URL", "http://restapi:8000")
FAST_URL = os.getenv("FASTAPI_URL", "http://fastapi:8001")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
QUEUE_NAME = os.getenv("QUEUE_NAME", "patients")

router = APIRouter()

# Cache de conexão RabbitMQ
_rabbit_connection = None

async def get_rabbitmq_channel():
    global _rabbit_connection
    if _rabbit_connection is None or _rabbit_connection.is_closed:
        _rabbit_connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await _rabbit_connection.channel()
    await channel.declare_queue(QUEUE_NAME, durable=True)
    return channel

# =============================================================================
# MODELS
# =============================================================================

class PatientMetadata(BaseModel):
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

class UpdatePatientRequest(BaseModel):
    patient_uuid: str
    first_name: Optional[str]
    last_name: Optional[str]
    birth_date: Optional[str]
    gender: Optional[str]

class EDFFileRequest(BaseModel):
    patient_iid: str
    session_name: str
    file_path: str
    patient_metadata: PatientMetadata
    additional_metadata: Optional[dict] = None

# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

async def authenticate_token(token: str) -> dict:
    """Autentica cientista via REST API"""
    try:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(f"{RESTAPI_URL}/restapi/scientists/profile/", headers=headers, timeout=10.0)
            if response.status_code == 200:
                scientist_data = response.json()
                return {
                    "scientist_id": scientist_data.get("id"),
                    "email": scientist_data.get("email"),
                    "is_verified": scientist_data.get("is_verified", False)
                }
            else:
                raise HTTPException(status_code=401, detail="Token inválido")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Authentication service is unavailable: {e}")

def prepare_fastapi_payload(enriched_data: dict) -> dict:
    """Prepara dados para envio ao FastAPI via RabbitMQ"""
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
    """Publica dados no RabbitMQ"""
    try:
        channel = await get_rabbitmq_channel()
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error on posting the message: {str(e)}")

# =============================================================================
# ENDPOINTS
# =============================================================================

@router.post("/register")
async def process_patient(
    request: ProcessPatientRequest,
    background_tasks: BackgroundTasks,
    authorization: Optional[str] = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication token is necessary")
    
    token = authorization.replace("Bearer ", "")
    auth_data = await authenticate_token(token)
    
    if not auth_data.get("is_verified", False):
        raise HTTPException(status_code=403, detail="Scientist is not verified")

    # Cria paciente no REST API
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
        resp = await client.post(
            f"{RESTAPI_URL}/restapi/patients/register/",
            json=patient_payload,
            headers={"Authorization": f"Bearer {token}"}
        )
        if resp.status_code != 201:
            raise HTTPException(status_code=resp.status_code, detail=resp.json().get("detail", resp.text))
        patient_data = resp.json()
        patient_iid = patient_data["patient_iid"]
        patient_uuid = patient_data.get("id")

    enriched_data = {
        "patient_iid": patient_iid,
        "scientist_id": auth_data["scientist_id"],
        "session_name": request.edf_file_data.get("session_name", "default_session") if request.edf_file_data else "default_session",
        "file_path": request.edf_file_data.get("file_path", "") if request.edf_file_data else "",
        "patient_metadata": request.patient_metadata.dict() if hasattr(request.patient_metadata, 'dict') else (request.patient_metadata or {}),
        "scientist_metadata": auth_data,
        "processing_timestamp": datetime.utcnow().isoformat()
    }

    background_tasks.add_task(publish_to_rabbitmq, enriched_data)

    return {"status": "success", "patient_iid": patient_iid, "patient_uuid": patient_uuid, "scientist_id": auth_data["scientist_id"]}

@router.get("/list")
async def list_patients(
    authorization: Optional[str] = Header(None),
    is_test: Optional[bool] = Query(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication token is necessary")
    
    token = authorization.replace("Bearer ", "")
    auth_data = await authenticate_token(token)
    
    params = {"is_test": str(is_test).lower()} if is_test is not None else {}
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{RESTAPI_URL}/restapi/patients/list/",
            headers={"Authorization": f"Bearer {token}"},
            params=params
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        
        patients_rest = resp.json()
        
        # Mapeia para o formato FastAPI
        patients_fast = [
            {
                "id": p["id"],
                "first_name": p["first_name"],
                "last_name": p["last_name"],
                "patient_iid": p["patient_iid"],
                "processing_status": "active" if p["is_active"] else "inactive"
            }
            for p in patients_rest
        ]
        
        return {
            "status": "success",
            "scientist_id": auth_data["scientist_id"],
            "patients": patients_fast
        }

@router.get("/available")
async def available_patients(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication token is necessary")
    
    token = authorization.replace("Bearer ", "")
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{RESTAPI_URL}/restapi/patients/available/", headers={"Authorization": f"Bearer {token}"})
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
    
@router.put("/update")
async def update_patient_gateway(
    payload: UpdatePatientRequest,
    authorization: Optional[str] = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication token is necessary")
    
    token = authorization.replace("Bearer ", "")
    auth_data = await authenticate_token(token)
    if not auth_data.get("is_verified", False):
        raise HTTPException(status_code=403, detail="Scientist is not verified")

    # Usar UUID do paciente na URL
    patient_id = payload.patient_uuid
    if not patient_id:
        raise HTTPException(status_code=400, detail="Its necessary sending patient_uuid")

    payload_dict = payload.dict()
    payload_dict.pop("patient_uuid")
    payload_dict["scientist_metadata"] = auth_data

    async with httpx.AsyncClient() as client:
        resp = await client.put(
            f"{RESTAPI_URL}/restapi/patients/scientist-update/{patient_id}/",
            json=payload_dict,
            headers={"Authorization": f"Bearer {token}"}
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)

    return {"status": "success", "patient": resp.json(), "scientist_id": auth_data["scientist_id"]}

# ----------- SOFT DELETE PATIENT VIA GATEWAY -----------
@router.delete("/delete/{patient_iid}")
async def soft_delete_patient_gateway(patient_iid: str, authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication token is necessary")
    
    token = authorization.replace("Bearer ", "")
    
    async with httpx.AsyncClient() as client:
        resp = await client.delete(
            f"{FAST_URL}/patients/{patient_iid}",  # endpoint do FastAPI que faz o soft delete
            headers={"Authorization": f"Bearer {token}"}
        )
        if resp.status_code not in [200, 204]:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
    
    return {"status": "success", "patient_iid": patient_iid}

# ----------- RESTORE PATIENT VIA GATEWAY -----------
@router.put("/restore/{patient_iid}")
async def restore_patient_gateway(patient_iid: str, authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication token is necessary")
    
    token = authorization.replace("Bearer ", "")
    
    async with httpx.AsyncClient() as client:
        resp = await client.put(
            f"{FAST_URL}/patients/{patient_iid}/restore",  # endpoint do FastAPI que faz o restore
            headers={"Authorization": f"Bearer {token}"}
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
    
    return {"status": "success", "patient_iid": patient_iid}