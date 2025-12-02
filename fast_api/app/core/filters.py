import mne
import logging

logger = logging.getLogger(__name__)


# ---------- HELPERS ----------
def apply_notch(raw: mne.io.BaseRaw, freqs: list[float]):
    raw.notch_filter(freqs=freqs)
    return raw

def apply_bandpass(raw: mne.io.BaseRaw, l_freq: float, h_freq: float):
    raw.filter(l_freq=l_freq, h_freq=h_freq)
    return raw


# ---------- STANDARD ----------
def standard_filter(raw: mne.io.BaseRaw) -> mne.io.BaseRaw:
    raw = apply_bandpass(raw, 1.0, 40.0)
    raw = apply_notch(raw, [50.0])
    logger.info("Filtro STANDARD aplicado (1–40 Hz + notch 50 Hz)")
    return raw


# ---------- AUTO ----------
def auto_filter(
    raw: mne.io.BaseRaw,
    patient_metadata: dict,
    trial_metadata: dict
) -> mne.io.BaseRaw:
    l_freq, h_freq = 0.5, 30.0

    if patient_metadata.get("age") and patient_metadata["age"] > 18:
        l_freq = 0.25

    raw = apply_bandpass(raw, l_freq, h_freq)
    raw = apply_notch(raw, [50.0])

    logger.info(
        f"Filtro AUTO aplicado ({l_freq}–{h_freq} Hz, notch 50 Hz) "
        f"→ metadados: patient={patient_metadata}, trial={trial_metadata}"
    )
    return raw


# ---------- CUSTOM ----------
def custom_filter(raw: mne.io.BaseRaw, config: dict) -> mne.io.BaseRaw:
    if config.get("highpass") or config.get("lowpass"):
        raw = apply_bandpass(
            raw,
            config.get("highpass", 0.5),
            config.get("lowpass", None)
        )
    if config.get("notch"):
        raw = apply_notch(raw, config["notch"])

    logger.info(f"Filtro CUSTOM aplicado → config={config}")
    return raw


# ---------- ROUTER ----------
def filter_data(
    raw: mne.io.BaseRaw,
    mode: str,
    config: dict | None = None,
    patient_metadata: dict | None = None,
    trial_metadata: dict | None = None,
) -> mne.io.BaseRaw:

# ---------- MODES -----------
    # Padrao
    if mode == "standard":
        return standard_filter(raw)
    # Automatico
    elif mode == "auto":
        return auto_filter(raw, patient_metadata or {}, trial_metadata or {})
    # Personalizavel
    elif mode == "custom":
        return custom_filter(raw, config or {})
    # Error
    else:
        raise ValueError(f"Modo de filtro inválido: {mode}")
