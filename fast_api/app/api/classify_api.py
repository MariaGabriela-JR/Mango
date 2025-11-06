from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
import logging
from pathlib import Path
from app.core.database import get_db
from app.core.models import Trial
from app.core.classification import classification_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/train", status_code=200)
def train_classifier(
    test_size: float = 0.3,
    random_state: int = 42,
    db: Session = Depends(get_db)
):
    """
    Treina o classificador usando os arquivos FIF filtrados.
    """
    try:
        trials = (
            db.query(Trial)
            .options(joinedload(Trial.edf_file))
            .all()
        )

        if not trials:
            raise HTTPException(status_code=404, detail="No trials found")

        result = classification_service.train_classifier(
            trials, db, test_size=test_size, random_state=random_state
        )

        return result

    except ValueError as e:
        logger.error(f"Erro de validação: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Erro interno durante treinamento")
        raise HTTPException(status_code=500, detail="Internal server error during training")


@router.get("/debug/files")
def debug_files(db: Session = Depends(get_db)):
    """
    Mostra todos os arquivos FIF detectados para cada trial (debug).
    """
    trials = db.query(Trial).all()
    file_info = []

    for trial in trials:
        if trial.edf_file:
            patient_iid = trial.edf_file.patient_iid
            edf_filename = Path(trial.edf_file.file_path).stem
            fif_path = classification_service.find_fif_file(patient_iid, edf_filename)

            file_info.append({
                "trial_id": str(trial.id),
                "patient_iid": patient_iid,
                "edf_filename": edf_filename,
                "fif_found": fif_path is not None,
                "fif_path": str(fif_path) if fif_path else None,
                "emotion_category": trial.emotion_category,
            })

    return file_info

