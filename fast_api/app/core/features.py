# core/features.py
import numpy as np
from scipy.signal import welch
from app.core.models import Trial as TrialModel, EDFFile as EDFFileModel
from app.core.database import SessionLocal


def extract_features_from_signal(signal, fs):
    """
    Extrai features simples para o KNN.
    Você pode expandir depois.
    """

    # PSD com Welch
    freqs, psd = welch(signal, fs=fs)

    def bandpower(low, high):
        idx = np.logical_and(freqs >= low, freqs <= high)
        return float(np.trapz(psd[idx], freqs[idx]))

    return {
        "delta": bandpower(0.5, 4),
        "theta": bandpower(4, 8),
        "alpha": bandpower(8, 13),
        "beta": bandpower(13, 30),
        "gamma": bandpower(30, 45),
        "mean": float(np.mean(signal)),
        "std": float(np.std(signal)),
    }


def extract_features_for_trial(trial: TrialModel, raw_signal, fs: int):
    """
    Conecta TrialModel ←→ dicionário de features.
    """
    features = extract_features_from_signal(raw_signal, fs)
    trial.parameters = features
    return features

