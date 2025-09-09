from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import EDFFile as EDFFileModel  
from app.schemas import EDFFileCreate, EDFFileUpdate, EDFFile as EDFFileSchema
import uuid

router = APIRouter()

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
    existing_file = db.query(EDFFileModel).filter(EDFFileModel.file_path == file_data.file_path).first()
    if existing_file:
        raise HTTPException(status_code=400, detail="File with this path already exists")
    
    db_file = EDFFileModel(**file_data.dict())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

@router.put("/{file_id}", response_model=EDFFileSchema)
def update_edf_file(file_id: uuid.UUID, file_data: EDFFileUpdate, db: Session = Depends(get_db)):
    db_file = db.query(EDFFileModel).filter(EDFFileModel.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="EDF file not found")
    
    for field, value in file_data.dict(exclude_unset=True).items():
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
