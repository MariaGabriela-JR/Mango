from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.models import EDFFile as EDFFileModel
from app.core.schemas import EDFFileCreate, EDFFileUpdate, EDFFile as EDFFileSchema
from app.core.preprocessing import validate_and_preprocess, EDFValidationError
from pathlib import Path
import uuid
import os

router = APIRouter()

def extract_metadata(raw, file_path: str):
    file_size = Path(file_path).stat().st_size

    annotations = []
    if len(raw.annotations) > 0:
        df = raw.annotations.to_data_frame()
        # converte para dict serializável
        annotations = df.to_dict(orient="records")
        # garante que timestamps virem string
        for ann in annotations:
            for k, v in ann.items():
                if hasattr(v, "isoformat"):  
                    ann[k] = v.isoformat()
                elif not isinstance(v, (str, int, float, type(None))):
                    ann[k] = str(v)

    return {
        "channels": raw.info["nchan"],
        "sample_frequency": float(raw.info["sfreq"]),
        "duration": float(raw.times[-1]),
        "recording_date": raw.info["meas_date"].isoformat() if raw.info["meas_date"] else None,
        "file_size": file_size,
        "metadata_json": {
            "channel_names": list(raw.info["ch_names"]),
            "bad_channels": list(raw.info.get("bads", [])),
            "annotations": annotations,
        }
    }

@router.get("/", response_model=list[EDFFileSchema])
def get_edf_files(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(EDFFileModel).offset(skip).limit(limit).all()


@router.get("/{file_id}", response_model=EDFFileSchema)
def get_edf_file(file_id: uuid.UUID, db: Session = Depends(get_db)):
    file = db.query(EDFFileModel).filter(EDFFileModel.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="EDF file not found")
    return file


@router.post("/", response_model=EDFFileSchema, status_code=status.HTTP_201_CREATED)
def create_edf_file(file_data: EDFFileCreate, db: Session = Depends(get_db)):
    # Evita duplicata
    existing_file = db.query(EDFFileModel).filter(EDFFileModel.file_path == file_data.file_path).first()
    if existing_file:
        raise HTTPException(status_code=400, detail="File with this path already exists")

    # Valida EDF com MNE
    try:
        raw = validate_and_preprocess(file_data.file_path)
    except EDFValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Coleta metadados
    meta = extract_metadata(raw, file_data.file_path)

    db_file = EDFFileModel(
        patient_iid=file_data.patient_iid,
        file_path=file_data.file_path,
        file_name=os.path.basename(file_data.file_path),
        **meta
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


@router.put("/{file_id}", response_model=EDFFileSchema)
def update_edf_file(file_id: uuid.UUID, file_data: EDFFileUpdate, db: Session = Depends(get_db)):
    db_file = db.query(EDFFileModel).filter(EDFFileModel.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="EDF file not found")

    # Caso `file_path` for atualizado, revalida + coleta novos metadados
    if file_data.file_path:
        try:
            raw = validate_and_preprocess(file_data.file_path)
            meta = extract_metadata(raw, file_data.file_path)
            for k, v in meta.items():
                setattr(db_file, k, v)
            db_file.file_name = os.path.basename(file_data.file_path)
        except EDFValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))

    for field, value in file_data.dict(exclude_unset=True, exclude={"file_path"}).items():
        setattr(db_file, field, value)

    db.commit()
    db.refresh(db_file)
    return db_file


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_edf_file(file_id: uuid.UUID, db: Session = Depends(get_db)):
    db_file = db.query(EDFFileModel).filter(EDFFileModel.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="EDF file not found")

    db.delete(db_file)
    db.commit()
    return

