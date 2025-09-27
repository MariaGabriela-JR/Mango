import base64
from typing import Dict, List, Optional
from collections import OrderedDict
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from .chunks import ChunkInfo, chunk_manager

class EEGPlotGenerator:
    def __init__(self, max_cache_size: int = 100):
        self.png_cache = OrderedDict()
        self.max_cache_size = max_cache_size
    
    def generate_chunk_plot(
        self, 
        file_path: str,
        chunk_info: ChunkInfo,
        width: int = 800,
        height: int = 400,
        channels: Optional[List[str]] = None
    ) -> Dict:
        cache_key = self._generate_cache_key(file_path, chunk_info.chunk_index, width, height, channels)
        
        if cache_key in self.png_cache:
            return self.png_cache[cache_key]
        
        result = self._create_plot(file_path, chunk_info, width, height, channels)
        self._update_cache(cache_key, result)
        return result
    
    def _create_plot(
        self, 
        file_path: str,
        chunk_info: ChunkInfo,
        width: int, 
        height: int,
        channels: Optional[List[str]] = None
    ) -> Dict:
        try:
            chunk_data = chunk_manager.get_chunk_data(file_path, chunk_info, channels)
            
            n_channels = len(chunk_data['channel_names'])
            if n_channels == 0:
                raise ValueError("Nenhum canal de dados disponível")
            channel_height = max(1.5, height / 100 / max(1, n_channels / 8))
            fig_height = channel_height * n_channels
            
            fig, axes = plt.subplots(n_channels, 1, figsize=(width/100, fig_height))
            if n_channels == 1:
                axes = [axes]
            
            for i, channel_name in enumerate(chunk_data['channel_names']):
                signal = chunk_data['data'][i, :]
                times = chunk_data['times']
                
                axes[i].plot(times, signal, linewidth=0.8, color='blue', alpha=0.8)
                axes[i].set_ylabel(channel_name, fontsize=9)
                axes[i].tick_params(axis='both', which='major', labelsize=7)
                axes[i].grid(True, alpha=0.3)
                axes[i].set_xlim(chunk_info.start_time, chunk_info.end_time)
            
            plt.xlabel('Tempo (segundos)', fontsize=10)
            
            channels_info = f"{n_channels} canais" 
            if channels and len(channels) != len(chunk_data['original_channels']):
                channels_info = f"{n_channels} de {len(chunk_data['original_channels'])} canais"
            
            plt.suptitle(
                f"EEG - Chunk {chunk_info.chunk_index + 1} "
                f"({chunk_info.start_time:.1f}s - {chunk_info.end_time:.1f}s) - {channels_info}",
                fontsize=11
            )
            plt.tight_layout()
            
            # Converte para base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            plt.close(fig)
            
            buffer.seek(0)
            png_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            return {
                'png_data': f"data:image/png;base64,{png_base64}",
                'channels_plotted': chunk_data['channel_names']
            }
            
        except Exception as e:
            plt.close('all')
            raise RuntimeError(f"Erro ao gerar plot: {str(e)}")
    
    def _generate_cache_key(self, file_path: str, chunk_index: int, 
                          width: int, height: int, channels: List[str]) -> str:
        import hashlib
        channel_key = "_".join(sorted(channels)) if channels else "all"
        key_string = f"{file_path}_{chunk_index}_{width}_{height}_{channel_key}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _update_cache(self, key: str, value: Dict):
        if key in self.png_cache:
            self.png_cache.pop(key)
        elif len(self.png_cache) >= self.max_cache_size:
            self.png_cache.popitem(last=False)
        self.png_cache[key] = value
    
    def clear_cache(self, file_path: str = None):
        if file_path:
            import hashlib
            keys_to_remove = []
            target_prefix = hashlib.md5(file_path.encode()).hexdigest()[:10]
            for key in list(self.png_cache.keys()):
                if key.startswith(target_prefix):
                    keys_to_remove.append(key)
            for key in keys_to_remove:
                self.png_cache.pop(key, None)
        else:
            self.png_cache.clear()

plot_generator = EEGPlotGenerator()
