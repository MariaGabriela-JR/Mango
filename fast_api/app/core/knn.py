# core/knn.py
import logging
from typing import List, Dict, Tuple

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

logger = logging.getLogger(__name__)


class KNNEmotionClassifier:
    """
    Treinador e preditor baseado em KNN para classificação de emoções
    usando os trials carregados pelo trial_builder.
    """

    def __init__(self, n_neighbors: int = 5):
        # Criamos um pipeline com normalização + KNN
        self.model = Pipeline([
            ("scaler", StandardScaler()),
            ("knn", KNeighborsClassifier(n_neighbors=n_neighbors))
        ])
        self._is_trained = False

    # ----------------------------------------------------------------------
    # Conversão dos trials para matriz X, y
    # ----------------------------------------------------------------------
    def _extract_xy_from_trials(self, trials: List[Dict]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Recebe trials como:
            {
                "start_time": ...,
                "duration": ...,
                "emotion_category": "happy/fear/neutral",
                "trial_index": int,
                "parameters": { ...features... }
            }

        E converte para X, y.
        """
        X = []
        y = []

        for t in trials:

            params = t.get("parameters", {})
            if not params:
                logger.warning(f"Trial sem features (parameters vazio): {t}")
                continue

            # transforma dict de params em vetor ordenado
            feature_vector = list(params.values())

            X.append(feature_vector)
            y.append(t["emotion_category"])

        if not X:
            raise ValueError("Nenhum trial possui parâmetros/feature para treinar o KNN.")

        X = np.array(X, dtype=float)
        y = np.array(y)

        logger.info(f"Extraído X com shape {X.shape} e y com shape {y.shape}")
        return X, y

    # ----------------------------------------------------------------------
    # Treino
    # ----------------------------------------------------------------------
    def train(self, trials: List[Dict]):
        """
        Treina o KNN usando uma lista de trials.
        """
        logger.info("Iniciando treino do KNN a partir dos trials...")

        X, y = self._extract_xy_from_trials(trials)

        self.model.fit(X, y)
        self._is_trained = True

        logger.info("Treino concluído!")
        logger.info(f"Classes treinadas: {set(y)}")

    # ----------------------------------------------------------------------
    # Predição para novos trials
    # ----------------------------------------------------------------------
    def predict(self, new_trials: List[Dict]) -> List[str]:
        """
        Recebe trials com 'parameters' e retorna a emoção prevista.
        """
        if not self._is_trained:
            raise RuntimeError("O modelo foi usado para prever antes de ser treinado.")

        X, _ = self._extract_xy_from_trials(new_trials)
        preds = self.model.predict(X)

        return preds.tolist()

    # ----------------------------------------------------------------------
    # Predição direta por vetor de features
    # ----------------------------------------------------------------------
    def predict_features(self, features: Dict) -> str:
        """
        Predição única passando apenas um dicionário de features.
        """
        if not self._is_trained:
            raise RuntimeError("Modelo não treinado")

        vector = np.array([list(features.values())], dtype=float)
        pred = self.model.predict(vector)
        return pred[0]

