# core/trial_builder.py
import pandas as pd
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

def map_trial_type_to_emotion(trial_type: str, stim_type: int) -> str:
    """
    Mapeia os valores do TSV para categorias de emoção válidas
    Baseado no seu protocolo experimental - AJUSTE CONFORME SEU EXPERIMENTO!
    """
    # Este é um exemplo - você precisa ajustar baseado no que cada trial_type representa
    mapping = {
        "n/a": "neutral",
        "rating": "neutral",      # momento de avaliação
        "vid": "happy",           # vídeo emocional - ajuste para a emoção correta
        "ima": "fear",            # imagery - ajuste conforme
        "fade": "neutral"         # transição
    }
    return mapping.get(trial_type, "neutral")

def load_trials_from_tsv(tsv_path: str) -> List[Dict]:
    try:
        df = pd.read_csv(tsv_path, sep='\t')
        
        print(f"DataFrame shape: {df.shape}")
        print(f"Actual columns: {list(df.columns)}")
        
        if df.empty:
            print("Warning: DataFrame is empty - no trials found")
            return []
        
        trials = []
        for _, row in df.iterrows():
            trial_type = str(row.get("trial_type", "n/a"))
            stim_type = int(row.get("stim_type", 0))
            
            trial_data = {
                "start_time": float(row.get("onset", 0.0)),
                "duration": float(row.get("duration", 0.0)),
                "emotion_category": map_trial_type_to_emotion(trial_type, stim_type),
                "trial_index": stim_type,  # usando stim_type como índice
                "description": f"Original trial_type: {trial_type}, stim_type: {stim_type}",
                "parameters": {},
            }
            trials.append(trial_data)
        
        print(f"Successfully loaded {len(trials)} trials from {tsv_path}")
        if trials:
            print(f"First trial emotion: {trials[0]['emotion_category']}")
        
        return trials
        
    except Exception as e:
        print(f"Error reading {tsv_path}: {str(e)}")
        return []
