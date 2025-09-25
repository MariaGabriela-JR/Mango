import aio_pika
import asyncio
import httpx
import json
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker")

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
QUEUE_NAME = os.getenv("QUEUE_NAME", "patients")
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://fastapi:8001")

async def call_fastapi_endpoint(endpoint: str, payload: dict):
    """Chama endpoints específicos do FastAPI"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        url = f"{FASTAPI_URL}{endpoint}"  # <-- não adiciona /fastapi manualmente
        logger.info(f"🌐 Chamando FastAPI: {url}")
        response = await client.post(url, json=payload)
        return response

async def process_patient_data(payload: dict):
    """Processa dados de paciente no FastAPI"""
    try:
        patient_data = payload.get("patient_data")
        if not patient_data:
            logger.error("❌ patient_data ausente no payload")
            return False

        patient_response = await call_fastapi_endpoint(
            "/api/patients/", 
            patient_data
        )

        if patient_response.status_code not in [200, 201]:
            logger.error(f"❌ Erro ao criar paciente: {patient_response.text}")
            return False

        # Se houver dados EDF, criar EDFFile
        edf_file_data = patient_data.get("edf_file_data")
        if edf_file_data:
            edf_response = await call_fastapi_endpoint(
                "/api/edf-files/", 
                edf_file_data
            )
            if edf_response.status_code not in [200, 201]:
                logger.error(f"❌ Erro ao criar EDF file: {edf_response.text}")
                return False

        logger.info("✅ Dados processados com sucesso no FastAPI")
        return True

    except Exception as e:
        logger.error(f"❌ Erro no processamento: {e}")
        return False

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            body = message.body.decode()
            payload = json.loads(body)
            logger.info(f"📦 Payload recebido: {payload}")

            action = payload.get("action", "")
            logger.info(f"📨 Mensagem recebida - Ação: {action}")

            if action == "process_patient_data":
                success = await process_patient_data(payload)
                if success:
                    logger.info("✅ Processamento concluído")
                else:
                    logger.error("❌ Falha no processamento")
            else:
                logger.warning(f"⚠️ Ação desconhecida: {action}")

        except Exception as e:
            logger.error(f"❌ Erro processando mensagem: {e}")

async def run_worker():
    logger.info("🚀 Iniciando worker...")

    while True:
        try:
            connection = await aio_pika.connect_robust(RABBITMQ_URL)
            logger.info("✅ Conectado ao RabbitMQ!")

            async with connection:
                channel = await connection.channel()
                await channel.set_qos(prefetch_count=1)

                queue = await channel.declare_queue(QUEUE_NAME, durable=True)
                logger.info(f"✅ Fila '{queue.name}' declarada")

                await queue.consume(process_message)
                logger.info("👂 Worker ouvindo mensagens...")

                await asyncio.Future()  # Mantém o worker rodando

        except Exception as e:
            logger.error(f"❌ Erro: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(run_worker())
