# core/classification_service.py
import os
import numpy as np
from pathlib import Path
from sqlalchemy.orm import Session
import logging
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

from app.core.models import Trial, ClassificationResult
import mne

logger = logging.getLogger(__name__)

class ClassificationService:
    def __init__(self, output_path: str = "/tmp/output"):
        self.OUTPUT_CONTAINER_PATH = Path(output_path)
        self.LABEL_MAP = {"ima": 1, "vid": 1, "rating": 0, "fade": 0}
    
    def find_fif_file(self, patient_iid: str, edf_filename: str) -> Path | None:
        """Encontra o arquivo FIF correspondente de forma robusta"""
        try:
            # Método 1: Busca pelo padrão esperado
            expected_pattern = f"{edf_filename}_filtered.fif"
            expected_path = self.OUTPUT_CONTAINER_PATH / patient_iid / expected_pattern
            
            if expected_path.exists():
                logger.info(f"Arquivo encontrado (método 1): {expected_path}")
                return expected_path
            
            # Método 2: Busca recursiva por qualquer arquivo FIF do paciente
            patient_dir = self.OUTPUT_CONTAINER_PATH / patient_iid
            if patient_dir.exists():
                fif_files = list(patient_dir.rglob("*.fif"))
                if fif_files:
                    logger.info(f"Arquivos FIF encontrados em {patient_dir}: {[f.name for f in fif_files]}")
                    return fif_files[0]  # Retorna o primeiro encontrado
            
            # Método 3: Busca em todo o output container
            all_fif_files = list(self.OUTPUT_CONTAINER_PATH.rglob(f"**/*{edf_filename}*.fif"))
            if all_fif_files:
                logger.info(f"Arquivo encontrado (busca global): {all_fif_files[0]}")
                return all_fif_files[0]
                
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar arquivo FIF para {patient_iid}/{edf_filename}: {str(e)}")
            return None
    
    def extract_features(self, fif_path: Path, trial_metadata=None) -> np.ndarray | None:
        """Extrai features do arquivo FIF"""
        try:
            raw = mne.io.read_raw_fif(fif_path, preload=True, verbose=False)
            
            # Aplica recorte temporal se metadados disponíveis
            if trial_metadata and hasattr(trial_metadata, 'start_time'):
                start_time = trial_metadata.start_time
                duration = getattr(trial_metadata, 'duration', 1.0)
                end_time = start_time + duration
                raw.crop(tmin=start_time, tmax=min(end_time, raw.times[-1]))
            
            data = raw.get_data()
            
            # Features mais robustas
            features = []
            for channel_data in data:
                channel_features = [
                    np.mean(np.abs(channel_data)),
                    np.std(channel_data),
                    np.max(np.abs(channel_data)),
                    np.median(channel_data),
                    np.mean(channel_data**2),  # Potência média
                ]
                features.extend(channel_features)
            
            return np.array(features)
            
        except Exception as e:
            logger.error(f"Erro ao extrair features de {fif_path}: {str(e)}")
            return None
    
    def prepare_training_data(self, trials, db: Session):
        """Prepara dados para treinamento"""
        X, y, trial_ids = [], [], []
        stats = {
            'total_trials': len(trials),
            'sem_edf_file': 0,
            'arquivo_nao_encontrado': 0,
            'erro_extracao': 0,
            'sucesso': 0
        }
        
        for trial in trials:
            if not trial.edf_file:
                stats['sem_edf_file'] += 1
                continue
            
            patient_iid = trial.edf_file.patient_iid
            edf_filename = Path(trial.edf_file.file_path).stem
            
            # Busca o arquivo FIF
            fif_path = self.find_fif_file(patient_iid, edf_filename)
            if not fif_path:
                stats['arquivo_nao_encontrado'] += 1
                logger.warning(f"Arquivo FIF não encontrado para trial {trial.id}")
                continue
            
            # Extrai features
            features = self.extract_features(fif_path, trial)
            if features is not None:
                X.append(features)
                y.append(self.LABEL_MAP.get(trial.emotion_category, 0))
                trial_ids.append(trial.id)
                stats['sucesso'] += 1
                logger.info(f"Features extraídas com sucesso para trial {trial.id}")
            else:
                stats['erro_extracao'] += 1
        
        logger.info(f"Estatísticas de preparação: {stats}")
        return np.array(X), np.array(y), trial_ids, stats
    
    def train_classifier(self, trials, db: Session, test_size=0.3, random_state=42):
        """Executa o treinamento do classificador"""
        if not trials:
            raise ValueError("Nenhum trial fornecido para treinamento")
        
        X, y, trial_ids, stats = self.prepare_training_data(trials, db)
        
        if len(X) < 2:
            raise ValueError(f"Dados insuficientes para treinamento. Apenas {len(X)} amostras válidas.")
        
        # Split dos dados
        (X_train, X_test, y_train, y_test, 
         trial_ids_train, trial_ids_test) = train_test_split(
            X, y, trial_ids, test_size=test_size, random_state=random_state
        )
        
        # Treina modelo
        clf = SVC(kernel="linear", random_state=random_state)
        clf.fit(X_train, y_train)
        
        # Predições
        preds = clf.predict(X_test)
        acc = accuracy_score(y_test, preds)
        
        # Salva resultados
        for i, (pred, true, trial_id) in enumerate(zip(preds, y_test, trial_ids_test)):
            result = ClassificationResult(
                trial_id=trial_id,
                predicted_label=str(pred),
                true_label=str(true),
                accuracy=acc,
                model_type="SVM_linear_filtered"
            )
            db.add(result)
        
        db.commit()
        
        return {
            "accuracy": float(acc),
            "samples_total": len(X),
            "samples_train": len(X_train),
            "samples_test": len(X_test),
            "feature_shape": X.shape[1],
            "stats": stats
        }

# Instância global do serviço
classification_service = ClassificationService()
