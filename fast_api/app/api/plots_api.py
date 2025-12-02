from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import uuid
from datetime import datetime
from typing import Optional
import os
from app.core.database import get_db
from app.core.models import EDFFile
from app.core.chunks import chunk_manager
from app.core.plots import plot_generator
from app.core.schemas import EEGChunkRequest, EEGPlotResponse, EEGChunkInfo

router = APIRouter(prefix="/plots", tags=["plots"])

@router.post("/eeg", response_model=EEGPlotResponse)
async def generate_eeg_plot(
    request: EEGChunkRequest,
    db: Session = Depends(get_db)
):
    edf_file = db.query(EDFFile).filter(EDFFile.id == request.edf_file_id).first()
    
    if not edf_file:
        raise HTTPException(status_code=404, detail="Arquivo EDF não encontrado no banco de dados")
    
    try:
        if not os.path.exists(edf_file.file_path):
            raise HTTPException(
                status_code=404, 
                detail=f"Arquivo físico não encontrado: {edf_file.file_path}"
            )
        
        edf_info = chunk_manager.read_edf_info(edf_file.file_path)
        
        chunks = chunk_manager.calculate_chunks(edf_info['duration'])
        
        if request.chunk_index >= len(chunks):
            raise HTTPException(
                status_code=400, 
                detail=f"Chunk {request.chunk_index} não existe. Arquivo tem {len(chunks)} chunks"
            )
        
        chunk_info = chunks[request.chunk_index]
        
        available_channels = edf_info['channel_names']
        
        if request.channels:
            invalid_channels = [ch for ch in request.channels if ch not in available_channels]
            
            if invalid_channels and len(invalid_channels) == len(request.channels):
                raise HTTPException(
                    status_code=400,
                    detail=f"Nenhum canal válido especificado. Canais disponíveis: {available_channels}"
                )
        
        plot_result = plot_generator.generate_chunk_plot(
            edf_file.file_path,
            chunk_info,
            request.width,
            request.height,
            request.channels
        )
        
        chunk_info_schema = EEGChunkInfo(
            chunk_index=chunk_info.chunk_index,
            start_time=chunk_info.start_time,
            end_time=chunk_info.end_time,
            duration=chunk_info.duration,
            is_full_chunk=chunk_info.is_full_chunk
        )
        
        return EEGPlotResponse(
            png_data=plot_result['png_data'],
            chunk_info=chunk_info_schema,
            channels_plotted=plot_result['channels_plotted'],
            generated_at=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar plot: {str(e)}")

@router.delete("/cache")
async def clear_plot_cache(
    edf_file_id: Optional[uuid.UUID] = Query(None, description="ID do EDF para limpar cache")
):
    plot_generator.clear_cache(str(edf_file_id) if edf_file_id else None)
    
    return {
        "message": f"Cache de plots {'completo' if not edf_file_id else 'do EDF ' + str(edf_file_id) + ' limpo'}"
    }
