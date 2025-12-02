from fastapi import APIRouter, Header, HTTPException, BackgroundTasks
from typing import Optional
from datetime import datetime
import httpx
import os
import json
import aio_pika
from pydantic import BaseModel
import uuid

from app.core.schemas import TrialCreate

RESTAPI_URL = os.getenv("RESTAPI_URL", "http://restapi:8000")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
QUEUE_NAME = os.getenv("QUEUE_NAME", "patients")

router = APIRouter()
_rabbit_connection = None

async def get_rabbitmq_channel():
    global _rabbit_connection
    if _rabbit_connection is None or _rabbit_connection.is_closed:
        _rabbit_connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await _rabbit_connection.channel()
    await channel.declare_queue(QUEUE_NAME, durable=True)
    return channel

async def authenticate_token(token: str) -> dict:
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
            raise HTTPException(status_code=401, detail="Invalid token")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Authentication service is unavailable: {str(e)}")

async def publish_trial_to_rabbitmq(enriched_data: dict):
    try:
        channel = await get_rabbitmq_channel()
        message_body = json.dumps(enriched_data).encode()

        await channel.default_exchange.publish(
            aio_pika.Message(
                body=message_body,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                headers={
                    "edf_file_id": enriched_data["trial_data"]["edf_file_id"],
                    "trial_index": enriched_data["trial_data"]["trial_index"],
                    "action": enriched_data["action"]
                }
            ),
            routing_key=QUEUE_NAME
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error on posting the message: {str(e)}")

@router.post("/process-trial")
async def process_trial(
    request: TrialCreate,
    background_tasks: BackgroundTasks,
    authorization: Optional[str] = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication token is necessary")

    token = authorization.replace("Bearer ", "")
    scientist = await authenticate_token(token)

    enriched_data = {
        "action": "process_trial_data",
        "scientist_metadata": {
            "scientist_id": scientist.get("id"),
            "email": scientist.get("email"),
            "is_verified": scientist.get("is_verified", False),
        },
        "trial_data": request.dict(),
        "processing_context": {
            "received_at": datetime.utcnow().isoformat()
        }
    }

    background_tasks.add_task(publish_trial_to_rabbitmq, enriched_data)

    return {
        "status": "queued",
        "edf_file_id": str(request.edf_file_id),
        "trial_index": request.trial_index,
        "timestamp": datetime.utcnow().isoformat()
    }
