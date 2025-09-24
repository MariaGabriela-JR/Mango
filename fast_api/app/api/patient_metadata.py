from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.core.models import PatientMetadata as PatientMetadataModel
from app.core.schemas import (
    PatientMetadataCreate,
    PatientMetadataUpdate,
    PatientMetadata,
    PatientMetadataSimple,  
)
from app.core.enums import ProcessingStatus

router = APIRouter()

# ---------- GET ALL ACTIVE PATIENTS ------------
@router.get("/", response_model=list[PatientMetadataSimple])
def get_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = (
        db.query(PatientMetadataModel)
        .filter(PatientMetadataModel.processing_status == ProcessingStatus.ACTIVE.value)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return patients


# ---------- GET SINGLE PATIENT ----------
@router.get("/{patient_iid}", response_model=PatientMetadata)
def get_patient(patient_iid: str, db: Session = Depends(get_db)):
    patient = (
        db.query(PatientMetadataModel)
        .filter(PatientMetadataModel.patient_iid == patient_iid)
        .first()
    )
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


# ---------- CREATE PATIENT ----------
@router.post("/", response_model=PatientMetadata, status_code=status.HTTP_201_CREATED)
def create_patient(patient_data: PatientMetadataCreate, db: Session = Depends(get_db)):
    existing_patient = (
        db.query(PatientMetadataModel)
        .filter(PatientMetadataModel.patient_iid == patient_data.patient_iid)
        .first()
    )
    if existing_patient:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")

    db_patient = PatientMetadataModel(**patient_data.dict())
    db_patient.processing_status = ProcessingStatus.ACTIVE.value
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


# ---------- UPDATE PATIENT ----------
@router.put("/{patient_iid}", response_model=PatientMetadata)
def update_patient(patient_iid: str, patient_data: PatientMetadataUpdate, db: Session = Depends(get_db)):
    db_patient = (
        db.query(PatientMetadataModel)
        .filter(PatientMetadataModel.patient_iid == patient_iid)
        .first()
    )
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    for field, value in patient_data.dict(exclude_unset=True).items():
        setattr(db_patient, field, value)

    if (patient_data.processing_status == ProcessingStatus.ACTIVE.value and 
        db_patient.processing_status == ProcessingStatus.DELETED.value):
        db_patient.deleted_at = None

    db.commit()
    db.refresh(db_patient)
    return db_patient


# ---------- SOFT DELETE PATIENT ----------
@router.delete("/{patient_iid}", status_code=status.HTTP_204_NO_CONTENT)
def soft_delete_patient(patient_iid: str, db: Session = Depends(get_db)):
    db_patient = (
        db.query(PatientMetadataModel)
        .filter(PatientMetadataModel.patient_iid == patient_iid)
        .first()
    )
    if not db_patient or db_patient.processing_status == ProcessingStatus.DELETED.value:
        raise HTTPException(status_code=404, detail="Patient not found or already deleted")

    db_patient.processing_status = ProcessingStatus.DELETED.value
    db_patient.deleted_at = datetime.utcnow()
    db.commit()
    return


# ---------- GET ALL DELETED PATIENTS ----------
@router.get("/deleted/all", response_model=list[PatientMetadataSimple])
def get_deleted_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = (
        db.query(PatientMetadataModel)
        .filter(PatientMetadataModel.processing_status == ProcessingStatus.DELETED.value)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return patients


# ---------- RESTORE DELETED PATIENT --------------
@router.put("/{patient_iid}/restore", response_model=PatientMetadata)
def restore_patient(patient_iid: str, db: Session = Depends(get_db)):
    db_patient = (
        db.query(PatientMetadataModel)
        .filter(PatientMetadataModel.patient_iid == patient_iid)
        .first()
    )
    if not db_patient or db_patient.processing_status != ProcessingStatus.DELETED.value:
        raise HTTPException(status_code=404, detail="Deleted patient not found")

    db_patient.processing_status = ProcessingStatus.ACTIVE.value
    db_patient.deleted_at = None
    db.commit()
    db.refresh(db_patient)
    return db_patient
