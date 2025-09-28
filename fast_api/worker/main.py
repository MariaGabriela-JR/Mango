# worker.py
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
FAST_URL = os.getenv("FASTAPI_URL", "http://fastapi:8001")
EDF_HOST_PATH = os.getenv("EDF_HOST_PATH")
EDF_CONTAINER_PATH = os.getenv("EDF_CONTAINER_PATH")

# ==============================
# FASTAPI CALLS
# ==============================
async def call_fastapi(endpoint: str, payload: dict):
    """Chama endpoints específicos do FastAPI"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        url = f"{FAST_URL}{endpoint}"
        logger.info(f"Calling FastAPI: {url} with payload: {payload}")
        response = await client.post(url, json=payload)
        return response

# ==============================
# PROCESSAMENTO
# ==============================
async def process_patient_data(payload: dict):
    """Processa dados de paciente + EDF no FastAPI"""
    try:
        patient_data = payload.get("patient_data")
        if not patient_data:
            logger.error("patient_data missing on payload")
            return False

        # --- 1. Criação/atualização do paciente ---
        patient_payload = {
            "patient_iid": patient_data["patient_iid"],
            "age": patient_data.get("age"),
            "gender": patient_data.get("gender"),
            "clinical_notes": patient_data.get("clinical_notes", "")
        }

        patient_resp = await call_fastapi("/api/patients/", patient_payload)
        if patient_resp.status_code not in [200, 201]:
            logger.error(f"Error in creating patient: {patient_resp.text}")
            return False
        logger.info(f"Patient created/updated: {patient_resp.json()}")


        # --- 2. Criação do EDF file ---
        # O endpoint /api/edf-files/ espera apenas estes campos:
        edf_payload = {
            "patient_iid": patient_data["patient_iid"],
            "session_name": patient_data.get("session_name", "default_session"),
            "file_path": patient_data["file_path"]
        }

        if EDF_HOST_PATH and EDF_CONTAINER_PATH:
            edf_payload["file_path"] = edf_payload["file_path"].replace(EDF_HOST_PATH, EDF_CONTAINER_PATH)

        file_path = patient_data["file_path"]
        if not os.path.isfile(file_path):
            logger.error(f"EDF file not found: {file_path}")

        edf_resp = await call_fastapi("/api/edf-files/", edf_payload)
        if edf_resp.status_code not in [200, 201]:
            try:
                err = edf_resp.json()
            except:
                err = edf_resp.text
            logger.error(f"Error at creating EDF file: {err}")
            return False
        logger.info(f"EDF file created: {edf_resp.json()}")

        return True

    except Exception as e:
        logger.error(f"Error on processing: {e}")
        return False
    
async def process_trial_data(payload: dict):
    """Processa Trials no FastAPI"""
    try:
        trial_data = payload.get("trial_data")
        if not trial_data:
            logger.error("trial_data missing on payload")
            return False

        # Apenas publica o payload no endpoint do FastAPI
        trial_resp = await call_fastapi("/api/trials/", trial_data)
        if trial_resp.status_code not in [200, 201]:
            try:
                err = trial_resp.json()
            except:
                err = trial_resp.text
            logger.error(f"Error at creating Trial: {err}")
            return False

        logger.info(f"Trial created: {trial_resp.json()}")
        return True

    except Exception as e:
        logger.error(f"Error on processing Trial: {e}")
        return False
    
async def process_chunks(payload: dict):
    """Processa chunks de um EDF file"""
    chunk_info = payload.get("chunk_info")
    if not chunk_info:
        logger.error("chunk_info missing")
        return False
    
    # Aqui você poderia chamar o endpoint /chunks no FastAPI
    chunk_resp = await call_fastapi("/chunks/edf/{edf_file_id}/summary".format(edf_file_id=payload.get("edf_file_id")), {})
    
    if chunk_resp.status_code not in [200, 201]:
        logger.error(f"Error processing chunks: {chunk_resp.text}")
        return False
    
    logger.info(f"Chunks processed: {chunk_resp.json()}")
    return True

async def process_plots(payload: dict):
    """Gera plots de EEG chunks"""
    plot_resp = await call_fastapi("/plots/eeg", payload)
    if plot_resp.status_code not in [200, 201]:
        logger.error(f"Error generating plot: {plot_resp.text}")
        return False

    logger.info(f"Plot generated: {plot_resp.json()}")
    return True


# ==============================
# RABBITMQ MESSAGE HANDLER
# ==============================
async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            payload = json.loads(message.body.decode())
            logger.info(f"Mensagem recebida: {payload}")

            action = payload.get("action")
            if action == "process_patient_data":
                success = await process_patient_data(payload)
            elif action == "process_trial_data":
                success = await process_trial_data(payload)
            else:
                logger.warning(f"Ação desconhecida: {action}")
                if success:
                    logger.info("Processing done with success")
                else:
                    logger.error("Fail on processing")

        except Exception as e:
            logger.error(f"Error at processing message: {e}")

# ==============================
# WORKER LOOP
# ==============================
async def run_worker():
    logger.info("Starting worker...")

    while True:
        try:
            connection = await aio_pika.connect_robust(RABBITMQ_URL)
            logger.info("Connected to RabbitMQ!")

            async with connection:
                channel = await connection.channel()
                await channel.set_qos(prefetch_count=1)
                queue = await channel.declare_queue(QUEUE_NAME, durable=True)
                logger.info(f"Queue '{queue.name}' created")

                await queue.consume(process_message)
                logger.info("Worker hearing messages...")

                await asyncio.Future()  # Mantém o worker rodando

        except Exception as e:
            logger.error(f"Error on main loop: {e}")
            await asyncio.sleep(5)

# ==============================
# ENTRYPOINT
# ==============================
if __name__ == "__main__":
    asyncio.run(run_worker())
