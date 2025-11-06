from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.core.models import Trial as TrialModel, EDFFile as EDFFileModel
from app.core.schemas import TrialCreate, TrialUpdate, Trial as TrialSchema, TrialSimple
import uuid
from pathlib import Path
from app.core.trial_builder import load_trials_from_tsv
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=list[TrialSimple])
def get_trials(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista trials com seus EDFs"""
    return (
        db.query(TrialModel)
        .options(joinedload(TrialModel.edf_file))
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{trial_id}", response_model=TrialSchema)
def get_trial(trial_id: uuid.UUID, db: Session = Depends(get_db)):
    """Retorna um trial específico"""
    trial = db.query(TrialModel).filter(TrialModel.id == trial_id).first()
    if not trial:
        raise HTTPException(status_code=404, detail="Trial not found")
    return trial


@router.post(
    "/auto/from_labels/{edf_file_id}",
    response_model=list[TrialSimple],
    status_code=status.HTTP_201_CREATED
)
def create_trials_from_labels(edf_file_id: uuid.UUID, db: Session = Depends(get_db)):
    """Cria automaticamente os trials a partir de um arquivo _labels.tsv"""
    edf_file = db.query(EDFFileModel).filter(EDFFileModel.id == edf_file_id).first()
    if not edf_file:
        raise HTTPException(status_code=404, detail="EDF file not found")

    label_path = edf_file.file_path.replace(".edf", "_labels.tsv")
    if not Path(label_path).exists():
        raise HTTPException(status_code=404, detail=f"Label file not found: {label_path}")

    trials_data = load_trials_from_tsv(label_path)
    created = []

    for trial_data in trials_data:
        trial = TrialModel(**trial_data, edf_file_id=edf_file.id)
        db.add(trial)
        created.append(trial)

    db.commit()

    trial_ids = [t.id for t in created]
    created = db.query(TrialModel).filter(TrialModel.id.in_(trial_ids)).all()

    edf_file.processing_status = "TRIALS_CREATED"
    db.commit()

    return [
        TrialSimple(
            id=t.id,
            edf_file_id=t.edf_file_id,
            patient_iid=t.edf_file.patient_iid if t.edf_file else None,
            emotion_category=t.emotion_category,
        )
        for t in created
    ]


@router.put("/{trial_id}", response_model=TrialSchema)
def update_trial(trial_id: uuid.UUID, trial_data: TrialUpdate, db: Session = Depends(get_db)):
    """Atualiza os dados de um trial"""
    db_trial = db.query(TrialModel).filter(TrialModel.id == trial_id).first()
    if not db_trial:
        raise HTTPException(status_code=404, detail="Trial not found")

    for field, value in trial_data.dict(exclude_unset=True).items():
        setattr(db_trial, field, value)

    db.commit()
    db.refresh(db_trial)
    return db_trial


@router.delete("/{trial_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trial(trial_id: uuid.UUID, db: Session = Depends(get_db)):
    """Remove um trial"""
    db_trial = db.query(TrialModel).filter(TrialModel.id == trial_id).first()
    if not db_trial:
        raise HTTPException(status_code=404, detail="Trial not found")

    db.delete(db_trial)
    db.commit()
    return

