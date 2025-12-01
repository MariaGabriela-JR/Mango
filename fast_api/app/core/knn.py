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
    KNN para classificação de emoções usando trials processados.
    Interface:
      - train(trials: List[Dict])
      - predict(trials: List[Dict]) -> List[str]
      - predict_from_params(params_list: List[Dict]) -> List[str]
    Os 'trials' devem ser dicts com chave "parameters" contendo um dict
    com pares feature_name -> value, e "emotion_category" com label.
    """

    def __init__(self, n_neighbors: int = 5):
        self.model = Pipeline([
            ("scaler", StandardScaler()),
            ("knn", KNeighborsClassifier(n_neighbors=n_neighbors))
        ])
        self._is_trained = False
        self._feature_order = None   # ordem fixa de features usada em treino/predição

    # ------------------------------------------------------
    # Converte os trials em X, y com FEATURE ORDER FIXA
    # ------------------------------------------------------
    def _extract_xy_from_trials(self, trials: List[Dict]) -> Tuple[np.ndarray, np.ndarray]:
        X = []
        y = []

        for t in trials:
            params = t.get("parameters", {})
            if not params:
                logger.warning(f"Trial sem parameters: {t}")
                continue

            # estabelece ordem fixa de features no primeiro trial válido
            if self._feature_order is None:
                # ordenação determinística por nome de chave
                self._feature_order = sorted(params.keys())

            # se aparecerem novas chaves ou faltar alguma, tentamos mapear via feature_order
            try:
                feature_vector = [params[k] for k in self._feature_order]
            except KeyError:
                # se keys diferentes, reconstrói feature_order usando interseção ordenada
                keys = sorted(params.keys())
                self._feature_order = keys
                feature_vector = [params[k] for k in self._feature_order]

            X.append(feature_vector)
            y.append(t["emotion_category"])

        if not X:
            raise ValueError("Nenhum trial possui features para treinar o KNN.")

        X = np.array(X, dtype=float)
        y = np.array(y)
        logger.info(f"KNN: extraído X.shape={X.shape}, y.shape={y.shape}, feature_order={self._feature_order}")
        return X, y

    # ------------------------------------------------------
    # Treino: recebe lista de trials (cada um com 'parameters' e 'emotion_category')
    # ------------------------------------------------------
    def train(self, trials: List[Dict]):
        X, y = self._extract_xy_from_trials(trials)
        self.model.fit(X, y)
        self._is_trained = True
        logger.info(f"KNN treinado com {len(y)} exemplos; classes: {set(y)}")

    # ------------------------------------------------------
    # Predição de lista de trials (cada trial contém 'parameters')
    # ------------------------------------------------------
    def predict(self, trials: List[Dict]) -> List[str]:
        if not self._is_trained:
            raise RuntimeError("Modelo não treinado")

        X = []
        for t in trials:
            params = t.get("parameters", {})
            if not params:
                raise ValueError("Trial sem parameters na predição")

            # assume _feature_order já definido no treino
            fv = [params[k] for k in self._feature_order]
            X.append(fv)

        X = np.array(X, dtype=float)
        return self.model.predict(X).tolist()

    # ------------------------------------------------------
    # Predição direta a partir de uma lista de dicts 'parameters' (sem wrapper trial)
    # ------------------------------------------------------
    def predict_from_params(self, params_list: List[Dict]) -> List[str]:
        if not self._is_trained:
            raise RuntimeError("Modelo não treinado")

        X = []
        for p in params_list:
            # certifica que todas as keys usadas sigam a mesma ordem do treino
            fv = [p[k] for k in self._feature_order]
            X.append(fv)

        X = np.array(X, dtype=float)
        return self.model.predict(X).tolist()

    # ------------------------------------------------------
    # Predição única por dict de features
    # ------------------------------------------------------
    def predict_features(self, features: Dict) -> str:
        if not self._is_trained:
            raise RuntimeError("Modelo não treinado")

        vect = [features[k] for k in self._feature_order]
        vect = np.array([vect], dtype=float)
        return self.model.predict(vect)[0]

