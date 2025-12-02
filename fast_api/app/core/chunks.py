from dataclasses import dataclass
from typing import List, Dict, Optional
import mne
import numpy as np

@dataclass
class ChunkInfo:
    chunk_index: int
    start_time: float
    end_time: float
    duration: float
    is_full_chunk: bool

class ChunkManager:
    
    @staticmethod
    def calculate_chunks(total_duration: float) -> List[ChunkInfo]:
        chunks = []
        
        if total_duration <= 900:  
            chunks.append(ChunkInfo(
                chunk_index=0,
                start_time=0,
                end_time=total_duration,
                duration=total_duration,
                is_full_chunk=True
            ))
        else:
            chunk_duration = 600  
            current_start = 0
            chunk_index = 0
            
            while current_start < total_duration:
                chunk_end = min(current_start + chunk_duration, total_duration)
                actual_duration = chunk_end - current_start
                
                chunks.append(ChunkInfo(
                    chunk_index=chunk_index,
                    start_time=current_start,
                    end_time=chunk_end,
                    duration=actual_duration,
                    is_full_chunk=(actual_duration >= chunk_duration)
                ))
                
                current_start = chunk_end
                chunk_index += 1
        
        return chunks
    
    @staticmethod
    def read_edf_info(file_path: str) -> Dict:
        try:
            raw = mne.io.read_raw_edf(file_path, preload=False, verbose=False)
            info = {
                'n_channels': len(raw.ch_names),
                'duration': raw.times[-1] if len(raw.times) > 0 else 0,
                'sample_rate': raw.info['sfreq'],
                'channel_names': raw.ch_names,
                'n_times': raw.n_times
            }
            raw.close()
            return info
        except Exception as e:
            raise RuntimeError(f"Erro ao ler arquivo EDF: {str(e)}")
    
    @staticmethod
    def get_chunk_data(file_path: str, chunk_info: ChunkInfo, channels: Optional[List[str]] = None) -> Dict:
        try:
            raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
            raw.crop(tmin=chunk_info.start_time, tmax=chunk_info.end_time)
            available_channels = raw.ch_names
            channels_to_plot = available_channels
            
            if channels:
                valid_channels = [ch for ch in channels if ch in available_channels]
                if valid_channels:
                    channels_to_plot = valid_channels
                    raw.pick(valid_channels)
                else:
                    channels_to_plot = available_channels
            
            data, times = raw.get_data(return_times=True)
            
            raw.close()
            
            return {
                'data': data,
                'times': times,
                'channel_names': channels_to_plot,  
                'sample_rate': raw.info['sfreq'],
                'n_samples': data.shape[1],
                'original_channels': available_channels 
            }
            
        except Exception as e:
            raise RuntimeError(f"Erro ao ler chunk do EDF: {str(e)}")
    
    @staticmethod
    def validate_edf_file(file_path: str) -> bool:
        try:
            raw = mne.io.read_raw_edf(file_path, preload=False, verbose=False)
            is_valid = len(raw.ch_names) > 0 and raw.n_times > 0
            raw.close()
            return is_valid
        except:
            return False

chunk_manager = ChunkManager()
