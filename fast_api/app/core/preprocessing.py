import logging
from pathlib import Path
import numpy as np
import mne

logger = logging.getLogger(__name__)


class EDFValidationError(Exception):
    """Erro customizado para arquivos EDF inválidos."""


def _check_channels(raw: mne.io.BaseRaw):
    """Verifica se o arquivo possui canais válidos."""
    if raw.info["nchan"] == 0:
        raise EDFValidationError("Arquivo EDF sem canais detectados.")


def _check_data(raw: mne.io.BaseRaw):
    """Verifica se os dados não contêm NaN, Inf ou canais com variância zero."""
    data, _ = raw[:]
    if not np.isfinite(data).all():
        raise EDFValidationError("Arquivo EDF contém valores inválidos (NaN/inf).")

    if np.any(data.std(axis=1) == 0):
        raise EDFValidationError("Canal com variância zero encontrado.")


def _normalize(raw: mne.io.BaseRaw) -> mne.io.BaseRaw:
    """Aplica normalização z-score por canal."""
    def zscore(channel_data):
        mean = channel_data.mean()
        std = channel_data.std()
        return (channel_data - mean) / std if std > 0 else channel_data

    raw.apply_function(zscore, picks="all", dtype=np.float64)
    return raw


def _set_standard_montage(raw: mne.io.BaseRaw):
    """Tenta aplicar a montagem padrão 10-20."""
    try:
        raw.set_montage("standard_1020", on_missing="ignore")
    except Exception as e:
        logger.warning(f"Não foi possível aplicar montagem padrão: {e}")


def validate_and_preprocess(file_path: str) -> mne.io.BaseRaw:
    """
    Carrega, valida e normaliza um arquivo EDF usando MNE.
    
    Args:
        file_path (str): Caminho para o arquivo EDF.

    Returns:
        mne.io.BaseRaw: Objeto Raw pronto para uso.

    Raises:
        EDFValidationError: Se o arquivo for inválido ou não puder ser processado.
    """
    file = Path(file_path)
    if not file.exists():
        raise EDFValidationError(f"Arquivo EDF não encontrado: {file_path}")

    try:
        raw = mne.io.read_raw_edf(file_path, preload=True, verbose="ERROR")
    except Exception as e:
        raise EDFValidationError(f"Erro ao carregar EDF: {e}")

    # --- Validações ---
    _check_channels(raw)
    _check_data(raw)

    # --- Normalização ---
    raw = _normalize(raw)

    # --- Padronização ---
    _set_standard_montage(raw)

    logger.info(
        f"Arquivo EDF '{file.name}' validado: "
        f"{raw.info['nchan']} canais, {raw.info['sfreq']} Hz, duração {raw.times[-1]:.1f}s"
    )

    return raw

