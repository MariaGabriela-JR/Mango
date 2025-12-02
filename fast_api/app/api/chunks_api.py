from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from typing import List
from app.core.database import get_db
from app.core.models import EDFFile
from app.core.chunks import chunk_manager
from app.core.schemas import EEGChunksSummaryResponse, EEGChunksResponse, EEGChunkInfo

router = APIRouter(prefix="/chunks", tags=["chunks"])

@router.get("/edf/{edf_file_id}/summary", response_model=EEGChunksSummaryResponse)
async def get_edf_chunks_summary(
    edf_file_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    edf_file = db.query(EDFFile).filter(EDFFile.id == edf_file_id).first()
    if not edf_file:
        raise HTTPException(status_code=404, detail="Arquivo EDF não encontrado")
    
    try:
        edf_info = chunk_manager.read_edf_info(edf_file.file_path)
        chunks = chunk_manager.calculate_chunks(edf_info['duration'])
        
        return EEGChunksSummaryResponse(
            edf_file_id=edf_file_id,
            total_duration=edf_info['duration'],
            chunk_count=len(chunks)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar EDF: {str(e)}")

@router.get("/edf/{edf_file_id}/chunk/{chunk_index}", response_model=EEGChunkInfo)
async def get_specific_chunk(
    edf_file_id: uuid.UUID,
    chunk_index: int,
    db: Session = Depends(get_db)
):
    edf_file = db.query(EDFFile).filter(EDFFile.id == edf_file_id).first()
    if not edf_file:
        raise HTTPException(status_code=404, detail="Arquivo EDF não encontrado")
    
    try:
        edf_info = chunk_manager.read_edf_info(edf_file.file_path)
        chunks = chunk_manager.calculate_chunks(edf_info['duration'])
        
        if chunk_index >= len(chunks):
            raise HTTPException(status_code=404, detail="Chunk não encontrado")
        
        chunk = chunks[chunk_index]
        
        return EEGChunkInfo(
            chunk_index=chunk.chunk_index,
            start_time=chunk.start_time,
            end_time=chunk.end_time,
            duration=chunk.duration,
            is_full_chunk=chunk.is_full_chunk
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar EDF: {str(e)}")
