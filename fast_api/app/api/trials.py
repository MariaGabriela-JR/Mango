from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.core.models import Trial as TrialModel, EDFFile as EDFFileModel 
from app.core.schemas import TrialCreate, TrialUpdate, Trial as TrialSchema, TrialSimple 
import uuid

router = APIRouter()

@router.get("/", response_model=list[TrialSimple])
def get_trials(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return (
        db.query(TrialModel)
        .options(joinedload(TrialModel.edf_file))
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{trial_id}", response_model=TrialSchema)
def get_trial(trial_id: uuid.UUID, db: Session = Depends(get_db)):
    trial = db.query(TrialModel).filter(TrialModel.id == trial_id).first()
    if not trial:
        raise HTTPException(status_code=404, detail="Trial not found")
    return trial

@router.post("/", response_model=TrialSchema, status_code=status.HTTP_201_CREATED)
def create_trial(trial_data: TrialCreate, db: Session = Depends(get_db)):
    edf_file = db.query(EDFFileModel).filter(EDFFileModel.id == trial_data.edf_file_id).first()
    if not edf_file:
        raise HTTPException(status_code=404, detail="EDF file not found")
    
    existing_trial = db.query(TrialModel).filter(
        TrialModel.edf_file_id == trial_data.edf_file_id,
        TrialModel.trial_index == trial_data.trial_index
    ).first()
    
    if existing_trial:
        raise HTTPException(status_code=400, detail="Trial with this index already exists for this EDF file")
    
    db_trial = TrialModel(**trial_data.dict())
    db.add(db_trial)
    db.commit()
    db.refresh(db_trial)
    return db_trial

@router.put("/{trial_id}", response_model=TrialSchema)
def update_trial(trial_id: uuid.UUID, trial_data: TrialUpdate, db: Session = Depends(get_db)):
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
    db_trial = db.query(TrialModel).filter(TrialModel.id == trial_id).first()
    if not db_trial:
        raise HTTPException(status_code=404, detail="Trial not found")
    
    db.delete(db_trial)
    db.commit()
    return


