# api/metrics_api.py
import uuid
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.models import Trial as TrialModel, EDFFile as EDFFileModel
from app.api.knn_api import knn_model
from app.core.metrics import real_knn_metrics

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/{edf_id}")
def get_knn_metrics(edf_id: uuid.UUID, db: Session = Depends(get_db)):

    if not knn_model._is_trained:
        raise HTTPException(status_code=400, detail="KNN não está treinado")

    edf = db.query(EDFFileModel).filter(EDFFileModel.id == edf_id).first()
    if not edf:
        raise HTTPException(status_code=404, detail="EDF não encontrado")

    trials = (
        db.query(TrialModel)
        .filter(TrialModel.edf_file_id == edf.id)
        .all()
    )

    if not trials:
        raise HTTPException(status_code=404, detail="Nenhum trial encontrado")

    params_list = []
    y_true = []

    for t in trials:
        if t.parameters:
            params_list.append(t.parameters)
            y_true.append(t.emotion_category)

    if not params_list:
        raise HTTPException(status_code=400, detail="Nenhum trial possui parameters")

    try:
        y_pred = knn_model.predict_from_params(params_list)
        accuracy, f1 = real_knn_metrics(y_true, y_pred)

        return {
            "edf_id": str(edf_id),
            "num_trials": len(params_list),
            "accuracy": accuracy,
            "f1score": f1
        }

    except Exception as e:
        logger.exception("Erro ao calcular métricas")
        raise HTTPException(status_code=500, detail=str(e))

