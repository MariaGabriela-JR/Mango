from sqlalchemy import (
    Column, String, Integer, Float, Text, ForeignKey,
    TIMESTAMP, BigInteger, SmallInteger, text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .enums import ProcessingStatus
from .database import Base


class PatientMetadata(Base):
    __tablename__ = "patient_metadata"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    patient_iid = Column(String(100), nullable=False, unique=True)
    age = Column(Integer)
    gender = Column(String(20))
    clinical_notes = Column(Text)
    additional_info = Column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    processing_status = Column(String(30), nullable=False, server_default=ProcessingStatus.NEW.value)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    edf_files = relationship("EDFFile", back_populates="patient", cascade="all, delete-orphan")


class EDFFile(Base):
    __tablename__ = "edf_files"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    patient_iid = Column(String(100), ForeignKey("patient_metadata.patient_iid", ondelete="CASCADE"), nullable=False, index=True)
    session_name = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False, unique=True)
    file_name = Column(String(255), nullable=False)
    file_size = Column(BigInteger)
    channels = Column(SmallInteger)
    sample_frequency = Column(Float)
    duration = Column(Float)
    recording_date = Column(TIMESTAMP(timezone=True))
    metadata_json = Column("metadata", JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    processing_status = Column(String(30), nullable=False, server_default=ProcessingStatus.NEW.value)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    trials = relationship("Trial", back_populates="edf_file", cascade="all, delete-orphan")
    patient = relationship("PatientMetadata", back_populates="edf_files")


class Trial(Base):
    __tablename__ = "trials"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    edf_file_id = Column(UUID(as_uuid=True), ForeignKey("edf_files.id", ondelete="CASCADE"), nullable=False, index=True)
    trial_index = Column(Integer, nullable=False)
    start_time = Column(Float, nullable=False)
    duration = Column(Float, nullable=False)
    emotion_category = Column(String(50), nullable=False)
    description = Column(Text)
    parameters = Column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    processing_status = Column(String(30), default=ProcessingStatus.NEW.value, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    edf_file = relationship("EDFFile", back_populates="trials")
    
    @property
    def patient_iid(self):
        return self.edf_file.patient_iid if self.edf_file else None

class ClassificationResult(Base):
    __tablename__ = "classification_results"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    trial_id = Column(UUID(as_uuid=True), ForeignKey("trials.id"), nullable=False)
    model_type = Column(String, default="SVM")
    predicted_label = Column(String)
    true_label = Column(String)
    accuracy = Column(Float)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    trial = relationship("Trial")

