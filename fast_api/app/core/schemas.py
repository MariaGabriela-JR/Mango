from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import uuid
from app.core.enums import ProcessingStatus, EmotionCategory

# EDF
class EDFFileBase(BaseModel):
    patient_iid: str = Field(..., max_length=100)
    file_path: str
    file_name: str = Field(..., max_length=255)
    file_size: Optional[int] = None
    channels: Optional[int] = Field(None, gt=0)
    sample_frequency: Optional[float] = Field(None, gt=0)
    duration: Optional[float] = Field(None, gt=0)
    recording_date: Optional[datetime] = None
    processing_status: ProcessingStatus = Field(default=ProcessingStatus.NEW)

class EDFFileCreate(EDFFileBase):
    pass

class EDFFileUpdate(BaseModel):
    processing_status: Optional[ProcessingStatus] = None

class EDFFile(EDFFileBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

# Trials
class TrialBase(BaseModel):
    trial_index: int
    start_time: float = Field(..., ge=0)
    duration: float = Field(..., gt=0)
    emotion_category: EmotionCategory
    description: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)

class TrialCreate(TrialBase):
    edf_file_id: uuid.UUID

class TrialUpdate(BaseModel):
    trial_index: Optional[int] = None
    start_time: Optional[float] = None
    duration: Optional[float] = None
    emotion_category: Optional[EmotionCategory] = None
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

class Trial(TrialBase):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}

# Patients
class PatientMetadataBase(BaseModel):
    patient_iid: str = Field(..., max_length=100)  # manter patient_iid para bater com models.py
    age: Optional[int] = Field(None, gt=0, lt=120)
    gender: Optional[str] = Field(None, max_length=20)
    clinical_notes: Optional[str] = None
    additional_info: Dict[str, Any] = Field(default_factory=dict)

class PatientMetadataCreate(PatientMetadataBase):
    pass

class PatientMetadataUpdate(BaseModel):
    age: Optional[int] = None
    gender: Optional[str] = None
    clinical_notes: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None

class PatientMetadata(PatientMetadataBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

# Relations
class EDFFileWithTrials(EDFFile):
    trials: List[Trial] = []

class PatientWithFiles(PatientMetadata):
    edf_files: List[EDFFile] = []

