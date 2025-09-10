from datetime import datetime
from sqlalchemy import (Column, String, Integer, Float, Text, TIMESTAMP, SmallInteger, BigInteger,ForeignKey, func, text)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base, relationship
import uuid

Base = declarative_base()

class EDFFile(Base):
    __tablename__ = "edf_files"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    patient_iid = Column(String(100), nullable=False, index=True)
    file_path = Column(Text, nullable=False, unique=True)
    file_name = Column(String(255), nullable=False)
    file_size = Column(BigInteger)
    channels = Column(SmallInteger)
    sample_frequency = Column(Float)
    duration = Column(Float)
    recording_date = Column(TIMESTAMP(timezone=True))
    metadata_json = Column(
        "metadata",
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb")
    )
    processing_status = Column(String(30), nullable=False, server_default="'new'")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    # relacionamento com trials
    trials = relationship("Trial", back_populates="edf_file", cascade="all, delete-orphan")


class PatientMetadata(Base):
    __tablename__ = "patient_metadata"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    patient_iid = Column(String(100), nullable=False, unique=True)
    age = Column(Integer)
    gender = Column(String(20))
    clinical_notes = Column(Text)
    additional_info = Column(JSONB, nullable=False, server_default="{}")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

class Trial(Base):
    __tablename__ = "trials"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    edf_file_id = Column(UUID(as_uuid=True), ForeignKey("edf_files.id", ondelete="CASCADE"), nullable=False, index=True)
    trial_index = Column(Integer, nullable=False)
    start_time = Column(Float, nullable=False)
    duration = Column(Float, nullable=False)
    emotion_category = Column(String(50), nullable=False)
    description = Column(Text)
    parameters = Column(JSONB, nullable=False, server_default="{}")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


    edf_file = relationship("EDFFile", back_populates="trials")

