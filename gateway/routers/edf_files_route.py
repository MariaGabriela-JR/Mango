from fastapi import APIRouter, HTTPException, Header, BackgroundTasks
from typing import Optional
from datetime import datetime
import httpx
import os
import json
import aio_pika
from pydantic import BaseModel

# =============================================================================
# CONFIGURAÇÕES
# =============================================================================
RESTAPI_URL = os.getenv("RESTAPI_URL", "http://restapi:8000")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
QUEUE_NAME = os.getenv("QUEUE_NAME", "patients")
FAST_URL = os.getenv("FAST_URL", "http://fastapi:8001")

router = APIRouter()

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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error on posting message: {str(e)}")

# =============================================================================
# ENDPOINT
# =============================================================================
@router.post("/process-edf-file")
async def process_edf_file(
    request: EDFFileRequest,
    background_tasks: BackgroundTasks,
    authorization: Optional[str] = Header(None)
):
    """Processa arquivo EDF - envia para RabbitMQ"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication token is necessary")

    token = authorization.replace("Bearer ", "")
    scientist = await authenticate_token(token)

    payload = {
        "action": "process_patient_data",
        "patient_data": {
            "patient_iid": request.patient_iid,
            "session_name": request.session_name,
            "file_path": request.file_path,
            "additional_metadata": request.additional_metadata,
        },
        "scientist_metadata": {
            "scientist_id": scientist.get("id"),
            "email": scientist.get("email"),
            "is_verified": scientist.get("is_verified", False),
        },
        "received_at": datetime.utcnow().isoformat()
    }

    background_tasks.add_task(publish_to_rabbitmq, payload)

    return {"status": "queued"}