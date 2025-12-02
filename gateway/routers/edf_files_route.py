from fastapi import APIRouter, HTTPException, Header, BackgroundTasks, Query, Depends
from typing import Optional, List
from datetime import datetime
import httpx
import os
import json
import aio_pika
from pydantic import BaseModel
import logging
from uuid import UUID

# =============================================================================
# CONFIGURAÇÕES
# =============================================================================
RESTAPI_URL = os.getenv("RESTAPI_URL", "http://restapi:8000")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
QUEUE_NAME = os.getenv("QUEUE_NAME", "patients")
FAST_URL = os.getenv("FAST_URL", "http://fastapi:8001")
EDF_HOST_PATH = os.getenv("EDF_HOST_PATH")
EDF_CONTAINER_PATH = os.getenv("EDF_CONTAINER_PATH")

router = APIRouter()

logger = logging.getLogger("gateway")
logging.basicConfig(level=logging.INFO)

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

class EDFFileRequest(BaseModel):
    patient_iid: str
    session_name: str
    file_path: str
    patient_metadata: Optional[PatientMetadata] = None
    additional_metadata: Optional[dict] = None

# Modelos para a resposta dos arquivos EDF
class EDFFileSimple(BaseModel):
    id: UUID
    patient_iid: str
    file_path: Optional[str] = None
    file_name: str
    session_name: str
    processing_status: str
    channels: Optional[str] = None
    sample_frequency: Optional[float] = None
    duration: Optional[float] = None
    recording_date: Optional[datetime] = None
    file_size: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class EDFFileResponse(BaseModel):
    id: UUID
    patient_iid: str
    file_path: str
    file_name: str
    session_name: str
    processing_status: str
    channels: int
    sample_frequency: float
    duration: float
    recording_date: Optional[datetime] = None
    file_size: int
    metadata_json: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

# =============================================================================
# AUTENTICAÇÃO
# =============================================================================
async def authenticate_token(token: str) -> dict:
    """Autentica o cientista via REST API"""
    try:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(
                f"{RESTAPI_URL}/restapi/scientists/profile/",
                headers=headers,
                timeout=10.0
            )
            if response.status_code == 200:
                return response.json()
            raise HTTPException(status_code=401, detail="Authentication token is invalid")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Authentication service is unavailable: {str(e)}")

async def get_current_scientist(authorization: Optional[str] = Header(None)):
    """Dependency para obter o cientista atual"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication token is necessary")
    
    token = authorization.replace("Bearer ", "")
    return await authenticate_token(token)

# =============================================================================
# ENDPOINTS EDF FILES
# =============================================================================

@router.post("/process-edf-file")
async def process_edf_file(
    request: EDFFileRequest,
    background_tasks: BackgroundTasks,
    authorization: Optional[str] = Header(None)
):
    """
    Processa arquivo EDF - recebe file_path do frontend
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication token is necessary")

    token = authorization.replace("Bearer ", "")
    scientist = await authenticate_token(token)

    logger.info(f"Processing EDF file request: {request}")

    try:
        # Converte o caminho do host para o caminho do container, se necessário
        file_path = request.file_path
        if EDF_HOST_PATH and EDF_CONTAINER_PATH:
            file_path = file_path.replace(EDF_HOST_PATH, EDF_CONTAINER_PATH)
            logger.info(f"Converted file path: {request.file_path} -> {file_path}")

        # Verifica se o arquivo existe (no contexto do container)
        if not os.path.isfile(file_path):
            logger.warning(f"File not found in container: {file_path}")
            # Mesmo se não existir no container, prossegue porque o worker vai verificar
            # O worker tem o mapeamento de volumes correto

        # Prepara o payload para o RabbitMQ
        payload = {
            "action": "process_patient_data",
            "patient_data": {
                "patient_iid": request.patient_iid,
                "session_name": request.session_name,
                "file_path": file_path,  # Usa o caminho convertido
                "additional_metadata": request.additional_metadata or {},
            },
            "scientist_metadata": {
                "scientist_id": scientist.get("id"),
                "email": scientist.get("email"),
                "is_verified": scientist.get("is_verified", False),
            },
            "received_at": datetime.utcnow().isoformat()
        }

        # Adiciona patient_metadata se disponível
        if request.patient_metadata:
            payload["patient_data"].update({
                "age": request.patient_metadata.age,
                "gender": request.patient_metadata.gender,
                "clinical_notes": request.patient_metadata.clinical_notes or ""
            })

        logger.info(f"Sending to RabbitMQ: {payload}")

        # Publica no RabbitMQ
        await publish_to_rabbitmq(payload)

        return {
            "status": "queued",
            "patient_iid": request.patient_iid,
            "session_name": request.session_name,
            "file_path": file_path,
            "message": "EDF file queued for processing"
        }

    except Exception as e:
        logger.error(f"Error processing EDF file: {e}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@router.get("/edf-files/", response_model=List[EDFFileSimple])
async def list_edf_files(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros por página"),
    authorization: Optional[str] = Header(None)
):
    """
    Lista todos os arquivos EDF ativos do FastAPI
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication token is necessary")

    token = authorization.replace("Bearer ", "")
    scientist = await authenticate_token(token)

    try:
        # Faz a requisição para o FastAPI
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{FAST_URL}/api/edf-files/",
                params={"skip": skip, "limit": limit},
                timeout=30.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error from FastAPI: {response.status_code} - {response.text}")
                raise HTTPException(status_code=response.status_code, detail=response.text)
                
    except httpx.RequestError as e:
        logger.error(f"Request error to FastAPI: {e}")
        raise HTTPException(status_code=503, detail="EDF Files service is unavailable")

@router.get("/edf-files/{file_id}", response_model=EDFFileResponse)
async def get_edf_file(
    file_id: UUID,
    authorization: Optional[str] = Header(None)
):
    """
    Obtém detalhes de um arquivo EDF específico
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication token is necessary")

    token = authorization.replace("Bearer ", "")
    scientist = await authenticate_token(token)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{FAST_URL}/api/edf-files/{file_id}",
                timeout=30.0
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                raise HTTPException(status_code=404, detail="EDF file not found")
            else:
                logger.error(f"Error from FastAPI: {response.status_code} - {response.text}")
                raise HTTPException(status_code=response.status_code, detail=response.text)
                
    except httpx.RequestError as e:
        logger.error(f"Request error to FastAPI: {e}")
        raise HTTPException(status_code=503, detail="EDF Files service is unavailable")

@router.get("/edf-files/deleted/all", response_model=List[EDFFileResponse])
async def get_deleted_edf_files(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros por página"),
    authorization: Optional[str] = Header(None)
):
    """
    Lista todos os arquivos EDF deletados
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication token is necessary")

    token = authorization.replace("Bearer ", "")
    scientist = await authenticate_token(token)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{FAST_URL}/api/edf-files/deleted/all",
                params={"skip": skip, "limit": limit},
                timeout=30.0
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error from FastAPI: {response.status_code} - {response.text}")
                raise HTTPException(status_code=response.status_code, detail=response.text)
                
    except httpx.RequestError as e:
        logger.error(f"Request error to FastAPI: {e}")
        raise HTTPException(status_code=503, detail="EDF Files service is unavailable")

# =============================================================================
# RABBITMQ
# =============================================================================

async def publish_to_rabbitmq(enriched_data: dict):
    """Publica dados formatados no RabbitMQ"""
    try:
        channel = await get_rabbitmq_channel()
        message_body = json.dumps(enriched_data).encode()

        await channel.default_exchange.publish(
            aio_pika.Message(
                body=message_body,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                headers={
                    "patient_iid": enriched_data["patient_data"]["patient_iid"],
                    "session_name": enriched_data["patient_data"]["session_name"],
                    "action": enriched_data["action"]
                }
            ),
            routing_key=QUEUE_NAME
        )
        logger.info(f"Message published to RabbitMQ for patient: {enriched_data['patient_data']['patient_iid']}")
    except Exception as e:
        logger.error(f"Error publishing to RabbitMQ: {e}")
        raise HTTPException(status_code=500, detail=f"Error on posting message: {str(e)}")