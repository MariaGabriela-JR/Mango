# api/knn_api.py
import uuid
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.models import Trial as TrialModel, EDFFile as EDFFileModel
from app.core.knn import KNNEmotionClassifier

router = APIRouter()
logger = logging.getLogger(__name__)

# Mantemos um modelo global (similar ao approach do classify_api)
knn_model = KNNEmotionClassifier(n_neighbors=5)


# ================================================================
# Treinar o modelo a partir de TODOS os trials do banco
# ================================================================
@router.post("/train", status_code=status.HTTP_200_OK)
def train_knn(db: Session = Depends(get_db)):
    """Treina o KNN usando todos os trials que já possuem features."""

    trials = db.query(TrialModel).all()

    if not trials:
        raise HTTPException(status_code=404, detail="Nenhum trial encontrado no banco")

    # Converte Trials do SQLAlchemy → lista de dicts compatíveis com core.knn
    trials_data = []
    for t in trials:
        trials_data.append({
            "start_time": t.start_time,
            "duration": t.duration,
            "emotion_category": t.emotion_category,
            "trial_index": t.trial_index,
            "parameters": t.parameters or {},   # precisa ter features!
        })

    try:
        knn_model.train(trials_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "status": "trained",
        "total_trials": len(trials_data),
        "classes": list(set(t["emotion_category"] for t in trials_data)),
    }


# ================================================================
# Prever emoções de trials específicos por ID
# ================================================================
@router.post("/predict/by_trial_ids")
def predict_by_trial_ids(trial_ids: list[uuid.UUID], db: Session = Depends(get_db)):
    """Recebe uma lista de IDs de trials e retorna as predições."""

    if not knn_model._is_trained:
        raise HTTPException(status_code=400, detail="Modelo não foi treinado ainda")

    db_trials = (
        db.query(TrialModel)
        .filter(TrialModel.id.in_(trial_ids))
        .all()
    )

    if not db_trials:
        raise HTTPException(status_code=404, detail="Nenhum trial encontrado")

    trials_data = []
    for t in db_trials:
        trials_data.append({
            "start_time": t.start_time,
            "duration": t.duration,
            "emotion_category": t.emotion_category,
            "trial_index": t.trial_index,
            "parameters": t.parameters or {},
        })

    preds = knn_model.predict(trials_data)

    return {
        "predictions": [
            {
                "trial_id": t.id,
                "true_emotion": t.emotion_category,
                "predicted_emotion": pred,
            }
            for t, pred in zip(db_trials, preds)
        ]
    }


# ================================================================
# Prever usando todos os trials pertencentes a um EDF
# ================================================================
@router.post("/predict/by_edf/{edf_id}")
def predict_by_edf(edf_id: uuid.UUID, db: Session = Depends(get_db)):
    """Prevê as emoções de todos os trials pertencentes a um EDF específico."""

    if not knn_model._is_trained:
        raise HTTPException(status_code=400, detail="Modelo não treinado")

    edf = db.query(EDFFileModel).filter(EDFFileModel.id == edf_id).first()
    if not edf:
        raise HTTPException(status_code=404, detail="EDF não encontrado")

    db_trials = db.query(TrialModel).filter(TrialModel.edf_file_id == edf.id).all()

    if not db_trials:
        raise HTTPException(status_code=404, detail="Nenhum trial para este EDF")

    trials_data = []
    for t in db_trials:
        trials_data.append({
            "start_time": t.start_time,
            "duration": t.duration,
            "emotion_category": t.emotion_category,
            "trial_index": t.trial_index,
            "parameters": t.parameters or {},
        })

    preds = knn_model.predict(trials_data)

    return {
        "edf_id": edf_id,
        "predictions": [
            {
                "trial_id": t.id,
                "true_emotion": t.emotion_category,
                "predicted_emotion": pred,
            }
            for t, pred in zip(db_trials, preds)
        ],
    }

