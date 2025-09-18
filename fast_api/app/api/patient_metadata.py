from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.models import PatientMetadata as PatientMetadataModel
from app.core.schemas import PatientMetadataCreate, PatientMetadataUpdate, PatientMetadata as PatientMetadataSchema
from app.core.enums import Gender
import uuid

router = APIRouter()

# ---------- GET ALL PATIENTS ----------
@router.get("/", response_model=list[PatientMetadataSchema])
def get_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(PatientMetadataModel).offset(skip).limit(limit).all()


# ---------- GET SINGLE PATIENT ----------
@router.get("/{patient_iid}", response_model=PatientMetadataSchema)
def get_patient(patient_iid: str, db: Session = Depends(get_db)):
    patient = db.query(PatientMetadataModel).filter(PatientMetadataModel.patient_iid == patient_iid).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


# ---------- CREATE PATIENT ----------
@router.post("/", response_model=PatientMetadataSchema, status_code=status.HTTP_201_CREATED)
def create_patient(patient_data: PatientMetadataCreate, db: Session = Depends(get_db)):
    existing_patient = db.query(PatientMetadataModel).filter(PatientMetadataModel.patient_iid == patient_data.patient_iid).first()
    if existing_patient:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")

    db_patient = PatientMetadataModel(**patient_data.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


# ---------- UPDATE PATIENT ----------
@router.put("/{patient_iid}", response_model=PatientMetadataSchema)
def update_patient(patient_iid: str, patient_data: PatientMetadataUpdate, db: Session = Depends(get_db)):
    db_patient = db.query(PatientMetadataModel).filter(PatientMetadataModel.patient_iid == patient_iid).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    for field, value in patient_data.dict(exclude_unset=True).items():
        setattr(db_patient, field, value)

    db.commit()
    db.refresh(db_patient)
    return db_patient


# ---------- DELETE PATIENT ----------
@router.delete("/{patient_iid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_iid: str, db: Session = Depends(get_db)):
    db_patient = db.query(PatientMetadataModel).filter(PatientMetadataModel.patient_iid == patient_iid).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    db.delete(db_patient)
    db.commit()
    return
