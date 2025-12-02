import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query
from app.core.preprocessing import validate_and_preprocess, EDFValidationError

router = APIRouter()

EDF_CONTAINER_PATH = Path(os.getenv("EDF_CONTAINER_PATH", "/data_mango"))

@router.get("/validate")
def validate_edf(file_name: str = Query(..., description="Nome do arquivo EDF")):
    file_path = EDF_CONTAINER_PATH / file_name
    try:
        raw = validate_and_preprocess(file_path)
    except EDFValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {e}")

    return {
        "status": "ok",
        "file": str(file_path),
        "n_channels": raw.info["nchan"],
        "sfreq": raw.info["sfreq"],
        "duration_sec": raw.times[-1],
        "ch_names": raw.info["ch_names"],
    }
