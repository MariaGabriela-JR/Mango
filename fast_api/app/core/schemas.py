
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import uuid
from app.core.enums import ProcessingStatus, EmotionCategory, Gender

# ---------- EDF FILE BASE ----------
class EDFFileCreateBase(BaseModel):
    patient_iid: str = Field(..., max_length=100)
    file_path: str

class EDFFileBase(EDFFileCreateBase):
    file_name: str = Field(..., max_length=255)
    file_size: Optional[int] = None
    channels: Optional[int] = Field(None, gt=0)
    sample_frequency: Optional[float] = Field(None, gt=0)
    duration: Optional[float] = Field(None, gt=0)
    recording_date: Optional[datetime] = None
    processing_status: ProcessingStatus = Field(default=ProcessingStatus.NEW)

# ---------- EDF FILE CREATE / UPDATE ----------
class EDFFileCreate(EDFFileCreateBase):
    pass

class EDFFileUpdate(BaseModel):
    file_path: Optional[str] = None
    processing_status: Optional[ProcessingStatus] = None

# ---------- EDF FILE RESPONSE ----------
class EDFFile(EDFFileBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    metadata_json: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"from_attributes": True}

# ---------- TRIAL BASE ----------
class TrialBase(BaseModel):
    trial_index: int
    start_time: float = Field(..., ge=0)
    duration: float = Field(..., gt=0)
    emotion_category: EmotionCategory
    description: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)

# ---------- TRIAL CREATE / UPDATE ----------
class TrialCreate(TrialBase):
    edf_file_id: uuid.UUID

class TrialUpdate(BaseModel):
    trial_index: Optional[int] = None
    start_time: Optional[float] = None
    duration: Optional[float] = None
    emotion_category: Optional[EmotionCategory] = None
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

# ---------- TRIAL RESPONSE ----------
class Trial(TrialBase):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}

# ---------- PATIENT METADATA BASE ----------
class PatientMetadataBase(BaseModel):
    patient_iid: str = Field(..., max_length=100)
    age: Optional[int] = Field(None, gt=0, lt=120)
    gender: Optional[Gender] = None  # enum
    clinical_notes: Optional[str] = None
    additional_info: Dict[str, Any] = Field(default_factory=dict)

# ---------- PATIENT CREATE ----------
class PatientMetadataCreate(PatientMetadataBase):
    pass

# ---------- PATIENT UPDATE ----------
class PatientMetadataUpdate(BaseModel):
    age: Optional[int] = None
    gender: Optional[Gender] = None  # enum
    clinical_notes: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None

# ---------- PATIENT RESPONSE ----------
class PatientMetadata(PatientMetadataBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
