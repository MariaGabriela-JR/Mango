from app.core.models import PatientMetadata, EDFFile, Trial

logger = logging.getLogger(__name__)

# -------------------------------
# 1. Filtros básicos de sinal
# -------------------------------

def apply_highpass(raw: mne.io.BaseRaw, freq: float) -> mne.io.BaseRaw:
    """Aplica filtro passa-alta."""
    raw.filter(l_freq=freq, h_freq=None)
    return raw

def apply_lowpass(raw: mne.io.BaseRaw, freq: float) -> mne.io.BaseRaw:
    """Aplica filtro passa-baixa."""
    raw.filter(l_freq=None, h_freq=freq)
    return raw

def apply_bandpass(raw: mne.io.BaseRaw, l_freq: float, h_freq: float) -> mne.io.BaseRaw:
    """Aplica filtro passa-banda."""
    raw.filter(l_freq=l_freq, h_freq=h_freq)
    return raw

def apply_notch(raw: mne.io.BaseRaw, freqs: list[float] = [50, 60]) -> mne.io.BaseRaw:
    """Remove interferência da rede elétrica (50/60 Hz)."""
    raw.notch_filter(freqs=freqs)
    return raw

# -------------------------------
# 2. Estratégias de filtragem
# -------------------------------

def auto_filter(raw: mne.io.BaseRaw, patient_metadata: dict, trial_metadata: dict) -> mne.io.BaseRaw:
    """
    Aplica um filtro automático baseado em metadados.
    Exemplos:
      - Idade < 18 → passa-banda (1–40 Hz)
      - Experimento 'resting_state' → notch + passa-banda (0.5–45 Hz)
      - Sessão 'sleep' → passa-baixa (30 Hz)
    """
    age = patient_metadata.get("age")
    gender = patient_metadata.get("gender")
    session = trial_metadata.get("session")
    experiment = trial_metadata.get("experiment_type")

    # Exemplo de regras simples
    if experiment == "resting_state":
        raw = apply_notch(raw, freqs=[50, 60])
        raw = apply_bandpass(raw, 0.5, 45)
    elif session == "sleep":
        raw = apply_lowpass(raw, 30)
    elif age and age < 18:
        raw = apply_bandpass(raw, 1, 40)
    else:
        # fallback genérico
        raw = apply_bandpass(raw, 0.5, 50)

    logger.info("Filtro automático aplicado com base nos metadados.")
    return raw


def raw_filter(raw: mne.io.BaseRaw) -> mne.io.BaseRaw:
    """
    Não aplica filtro algum.
    Retorna apenas os dados crus (já validados no preprocessing).
    """
    logger.info("Modo CRU: sem filtragem aplicada.")
    return raw


def custom_filter(raw: mne.io.BaseRaw, config: dict) -> mne.io.BaseRaw:
    """
    Aplica filtros definidos manualmente pelo usuário.
    Exemplo de config:
        {
            "highpass": 1.0,
            "lowpass": 40.0,
            "notch": [50, 60]
        }
    """
    if "highpass" in config:
        raw = apply_highpass(raw, config["highpass"])
    if "lowpass" in config:
        raw = apply_lowpass(raw, config["lowpass"])
    if "bandpass" in config:
        l, h = config["bandpass"]
        raw = apply_bandpass(raw, l, h)
    if "notch" in config:
        raw = apply_notch(raw, freqs=config["notch"])

    logger.info(f"Filtro customizado aplicado: {config}")
    return raw

# -------------------------------
# 3. Função principal
# -------------------------------

def filter_data(
    raw: mne.io.BaseRaw,
    mode: str = "auto",
    patient_metadata: dict | None = None,
    trial_metadata: dict | None = None,
    config: dict | None = None,
) -> mne.io.BaseRaw:
    """
    Seleciona a estratégia de filtragem.
    
    Args:
        raw: objeto MNE Raw já carregado/validado.
        mode: "auto" | "raw" | "custom"
        patient_metadata: dicionário com informações do paciente
        trial_metadata: dicionário com informações do trial/experimento
        config: dicionário com parâmetros do filtro (apenas no modo "custom")
    """
    if mode == "raw":
        return raw_filter(raw)
    elif mode == "custom":
        if not config:
            raise ValueError("Modo 'custom' requer argumento 'config'.")
        return custom_filter(raw, config)
    else:  # default: auto
        return auto_filter(raw, patient_metadata or {}, trial_metadata or {})
