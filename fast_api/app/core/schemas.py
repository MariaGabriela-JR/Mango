from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import uuid
from app.core.enums import ProcessingStatus, EmotionCategory, Gender

# -------------------- TRIAL -------------------------------

class TrialBase(BaseModel):
    trial_index: int
    start_time: float = Field(..., ge=0)
    duration: float = Field(..., gt=0)
    emotion_category: EmotionCategory
    description: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)


class TrialCreate(TrialBase):
    edf_file_id: uuid.UUID


class TrialSimple(BaseModel):
    id: uuid.UUID
    edf_file_id: uuid.UUID
    patient_iid: str
    emotion_category: str

    model_config = {"from_attributes": True}
  

class TrialUpdate(BaseModel):
    trial_index: Optional[int] = None
    start_time: Optional[float] = None
    duration: Optional[float] = None
    emotion_category: Optional[EmotionCategory] = None
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    processing_status: Optional[ProcessingStatus] = None


class Trial(TrialBase):
    id: uuid.UUID
    edf_file_id: uuid.UUID
    patient_iid: str
    processing_status: ProcessingStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# -------------------- EDF FILE ----------------------------

class EDFFileCreateBase(BaseModel):
    patient_iid: str = Field(..., max_length=100)
    session_name: str = Field(..., max_length=100)
    file_path: str


class EDFFileSimple(BaseModel):
    id: uuid.UUID
    patient_iid: str
    file_name: str
    session_name: str
    processing_status: ProcessingStatus

    model_config = {"from_attributes": True}


class EDFFileBase(EDFFileCreateBase):
    file_name: str = Field(..., max_length=255)
    file_size: Optional[int] = None
    channels: Optional[int] = Field(None, gt=0)
    sample_frequency: Optional[float] = Field(None, gt=0)
    duration: Optional[float] = Field(None, gt=0)
    recording_date: Optional[datetime] = None
    processing_status: ProcessingStatus = Field(default=ProcessingStatus.NEW)


class EDFFileCreate(EDFFileCreateBase):
    pass


class EDFFileUpdate(BaseModel):
    file_path: Optional[str] = None
    session_name: Optional[str] = None
    processing_status: Optional[ProcessingStatus] = None
    metadata_json: Optional[Dict[str, Any]] = None


class EDFFile(EDFFileBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    metadata_json: Dict[str, Any] = Field(default_factory=dict)
    trials: List[Trial] = []

    model_config = {"from_attributes": True}



# -------------------- PATIENT METADATA --------------------

# Schema simplificado para listagem
class PatientMetadataSimple(BaseModel):
    id: uuid.UUID
    patient_iid: str
    processing_status: ProcessingStatus

    model_config = {"from_attributes": True}


# Schema base completo
class PatientMetadataBase(BaseModel):
    patient_iid: str = Field(..., max_length=100)
    age: Optional[int] = Field(None, gt=0, lt=120)
    gender: Optional[Gender] = None
    clinical_notes: Optional[str] = None
    additional_info: Dict[str, Any] = Field(default_factory=dict)
    processing_status: ProcessingStatus = Field(default=ProcessingStatus.NEW)


class PatientMetadataCreate(PatientMetadataBase):
    pass


class PatientMetadataUpdate(BaseModel):
    age: Optional[int] = None
    gender: Optional[Gender] = None
    clinical_notes: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None
    processing_status: Optional[ProcessingStatus] = None


class PatientMetadata(PatientMetadataBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# -------------------- CHUNKS --------------------

class EEGChunkInfo(BaseModel):
    chunk_index: int
    start_time: float
    end_time: float
    duration: float
    is_full_chunk: bool

class EEGChunksSummaryResponse(BaseModel):
    edf_file_id: uuid.UUID
    total_duration: float
    chunk_count: int


class EEGChunkRequest(BaseModel):
    edf_file_id: uuid.UUID
    chunk_index: int
    width: int = 800
    height: int = 400
    channels: Optional[List[str]] = None

class EEGChunksResponse(BaseModel):
    edf_file_id: uuid.UUID
    total_duration: float
    sample_frequency: float
    channel_labels: List[str]
    chunks: List[EEGChunkInfo]
    chunk_count: int

class EEGPlotResponse(BaseModel):
    png_data: str
    chunk_info: EEGChunkInfo
    generated_at: datetime
