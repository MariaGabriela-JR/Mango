import aio_pika
import asyncio
import httpx
import json
import logging
import os
import mne
import numpy as np
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker_final")

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
QUEUE_NAME = os.getenv("QUEUE_NAME", "patients")
FAST_URL = os.getenv("FASTAPI_URL", "http://fastapi:8001")

# ==============================
# CORREÇÃO DO JSON SERIALIZATION
# ==============================

class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy types"""
    def default(self, obj: Any) -> Any:
        if isinstance(obj, (np.integer, np.int32, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        return super().default(obj)

def sanitize_for_json(data: Any) -> Any:
    """Converte todos os tipos numpy para tipos Python nativos"""
    if isinstance(data, dict):
        return {k: sanitize_for_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_for_json(item) for item in data]
    elif isinstance(data, (np.integer, np.int32, np.int64)):
        return int(data)
    elif isinstance(data, (np.floating, np.float32, np.float64)):
        return float(data)
    elif isinstance(data, np.ndarray):
        return data.tolist()
    elif isinstance(data, np.bool_):
        return bool(data)
    else:
        return data

# ==============================
# FUNÇÕES CORRIGIDAS
# ==============================

async def call_api(endpoint: str, payload: dict, method: str = "POST", timeout: float = 10.0):
    """Função corrigida com serialização segura"""
    try:
        # Sanitiza o payload para JSON
        safe_payload = sanitize_for_json(payload)
        
        async with httpx.AsyncClient() as client:
            if method.upper() == "POST":
                response = await client.post(
                    f"{FAST_URL}{endpoint}", 
                    json=safe_payload, 
                    timeout=timeout
                )
            elif method.upper() == "PUT":
                response = await client.put(
                    f"{FAST_URL}{endpoint}", 
                    json=safe_payload, 
                    timeout=timeout
                )
            else:
                raise ValueError(f"Unsupported method: {method}")
            return response
    except Exception as e:
        logger.warning(f"API call failed: {e}")
        return None

async def process_edf_metadata_only(file_path: str, patient_iid: str, session_name: str) -> bool:
    """Apenas metadados - com serialização segura"""
    try:
        logger.info(f"Extracting metadata from: {file_path}")
        
        if not os.path.isfile(file_path):
            logger.error(f"File not found: {file_path}")
            return False

        # Carrega apenas cabeçalho (RÁPIDO)
        raw = mne.io.read_raw_edf(file_path, preload=False, verbose=False)
        
        # Extrai metadados e converte para tipos Python nativos
        metadata = {
            "n_times": int(raw.n_times),  # Converte explicitamente para int
            "sfreq": float(raw.info['sfreq']),  # Converte explicitamente para float
            "n_channels": int(len(raw.ch_names)),
            "channel_names": raw.ch_names,  # Lista de strings já é segura
            "duration_seconds": float(raw.n_times / raw.info['sfreq']),
            "file_size_bytes": int(os.path.getsize(file_path))
        }
        
        raw.close()
        
        # Envia metadados
        payload = {
            "patient_iid": patient_iid,
            "session_name": session_name,
            "file_path": file_path,
            "metadata": metadata,
            "status": "metadata_extracted"
        }
        
        resp = await call_api("/api/edf-files/", payload)
        if resp and resp.status_code in [200, 201]:
            logger.info(f"Metadata extracted successfully: {file_path}")
            return True
        else:
            error_msg = resp.text if resp else "No response"
            logger.warning(f"Failed to save metadata: {error_msg}")
            return False
        
    except Exception as e:
        logger.error(f"Metadata extraction error: {e}")
        return False

async def process_patient_data_simple(payload: dict):
    """Processamento SIMPLES - apenas registros básicos"""
    try:
        patient_data = payload.get("patient_data")
        if not patient_data:
            logger.error("No patient_data in payload")
            return False

        patient_iid = patient_data["patient_iid"]
        
        # 1. Cria/atualiza paciente
        patient_payload = {
            "patient_iid": patient_iid,
            "age": patient_data.get("age"),
            "gender": patient_data.get("gender"),
            "clinical_notes": patient_data.get("clinical_notes", "")
        }

        # Tenta criar paciente
        patient_resp = await call_api("/api/patients/", patient_payload)
        
        # Se já existe, faz update
        if patient_resp and patient_resp.status_code == 400 and "already exists" in patient_resp.text:
            logger.info("Patient exists, updating...")
            update_resp = await call_api(f"/api/patients/{patient_iid}", patient_payload, "PUT")
            if not update_resp or update_resp.status_code != 200:
                logger.warning("Patient update failed, but continuing...")

        # 2. Se não tem arquivo, retorna sucesso
        if not patient_data.get("file_path"):
            logger.info("No file path, completed successfully")
            return True

        file_path = patient_data["file_path"]
        
        # 3. Verifica se arquivo existe
        if not os.path.isfile(file_path):
            logger.error(f"EDF file not found: {file_path}")
            return False

        # 4. Apenas extrai metadados (LEVE)
        logger.info("Starting metadata extraction...")
        metadata_success = await process_edf_metadata_only(
            file_path=file_path,
            patient_iid=patient_iid,
            session_name=patient_data.get("session_name", "default_session")
        )

        if metadata_success:
            logger.info("Metadata extraction completed")
            return True
        else:
            logger.error("Metadata extraction failed")
            # Mesmo se a extração de metadados falhar, consideramos sucesso
            # para não bloquear o processamento
            return True

    except Exception as e:
        logger.error(f"Error in simple processing: {e}")
        return False

# ==============================
# MESSAGE HANDLER
# ==============================

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            payload = json.loads(message.body.decode())
            patient_iid = payload.get('patient_data', {}).get('patient_iid', 'unknown')
            action = payload.get("action")
            
            logger.info(f"Processing: {patient_iid}, action: {action}")

            success = False
            
            if action == "process_patient_data":
                success = await process_patient_data_simple(payload)
            else:
                logger.warning(f"Unknown action: {action}")
                success = True  # Considera sucesso para ações desconhecidas

            if success:
                logger.info(f"Completed successfully: {patient_iid}")
            else:
                logger.error(f"Failed: {patient_iid}")

        except Exception as e:
            logger.error(f"Message processing error: {e}")

# ==============================
# WORKER LOOP
# ==============================

async def run_worker():
    logger.info("Starting FINAL worker - METADATA ONLY with JSON FIX")
    
    while True:
        try:
            connection = await aio_pika.connect_robust(RABBITMQ_URL)
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=1)
            queue = await channel.declare_queue(QUEUE_NAME, durable=True)

            await queue.consume(process_message)
            logger.info("Final worker ready and listening...")

            # Mantém o worker rodando
            await asyncio.Future()

        except Exception as e:
            logger.error(f"Connection error: {e}")
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(run_worker())