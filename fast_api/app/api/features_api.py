# api/features_api.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import numpy as np

from app.core.database import get_db
from app.core.models import Trial as TrialModel, EDFFile as EDFFileModel
from app.core.features import extract_features_for_trial

router = APIRouter()


@router.post("/generate/{edf_id}")
def generate_features(edf_id: str, db: Session = Depends(get_db)):
    """
    Gera features para todos os trials de um EDF.
    """
    edf = db.query(EDFFileModel).filter(EDFFileModel.id == edf_id).first()
    if not edf:
        raise HTTPException(status_code=404, detail="EDF não encontrado")

    # TODO: carregar o EDF real — por enquanto mock simples para demonstrar:
    fs = 256
    duration = 2  # 2 segundos só para exemplo
    fake_signal = np.random.randn(duration * fs)

    trials = db.query(TrialModel).filter(TrialModel.edf_file_id == edf.id).all()
    if not trials:
        raise HTTPException(status_code=404, detail="Nenhum trial associado ao EDF")

    updated = []
    for t in trials:
        extract_features_for_trial(t, fake_signal, fs)
        updated.append(t.id)

    db.commit()

    return {
        "status": "ok",
        "updated_trials": updated,
    }

