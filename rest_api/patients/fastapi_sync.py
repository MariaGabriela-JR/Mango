import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

FASTAPI_URL = getattr(settings, "FASTAPI_URL", "http://fastapi_app:8001/api/patients/")

def sync_patient_to_fastapi(patient_data: dict, scientist_id: str = None):
    """
    Envia os dados do paciente para o FastAPI.
    """
    headers = {}
    if scientist_id:
        headers["X-Scientist-ID"] = str(scientist_id)

    try:
        response = requests.post(
            FASTAPI_URL,
            json=patient_data,
            headers=headers,
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Erro ao sincronizar com FastAPI: {e}")
        return None