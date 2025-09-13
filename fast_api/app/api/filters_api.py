import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query
from app.core.preprocessing import validate_and_preprocess, EDFValidationError
import mne

router = APIRouter()

EDF_CONTAINER_PATH = Path(os.getenv("EDF_CONTAINER_PATH", "/data_mango"))
OUTPUT_CONTAINER_PATH = Path(os.getenv("OUTPUT_CONTAINER_PATH", "/code/output"))

@router.get("/discover")

def discover_files():
    if not EDF_CONTAINER_PATH.exists():
        raise HTTPException(status_code=500, detail=f"Pasta base não encontrada: {EDF_CONTAINER_PATH}")

    discovered = []
    for f in EDF_CONTAINER_PATH.rglob("*.edf"):
        discovered.append({
            "file_name": f.name,
            "file_path": str(f),
            "exists_on_disk": True
        })
    return discovered

# --- Aplicar filtros ---
@router.post("/{file_name}/apply")
def apply_filters(
    file_name: str,
    mode: str = Query("standard", enum=["raw", "standard", "custom"]),
    l_freq: float | None = Query(None, description="Frequência de corte passa-alta"),
    h_freq: float | None = Query(None, description="Frequência de corte passa-baixa"),
    notch: float | None = Query(None, description="Frequência notch (ex: 50 ou 60Hz)"),
):

    found_files = list(EDF_CONTAINER_PATH.rglob(file_name))
    
    found_files = [f for f in found_files if f.is_file() and f.name == file_name]

    if not found_files:
        raise HTTPException(status_code=404, detail=f"Arquivo não encontrado: {file_name}")
    if len(found_files) > 1:
        paths = [str(f) for f in found_files]
        raise HTTPException(
            status_code=400,
            detail=f"Múltiplos arquivos com o nome {file_name} encontrados: {paths}"
        )

    file_path = found_files[0]

    # 2. Carregar e validar arquivo EDF
    try:
        raw = validate_and_preprocess(file_path)
    except EDFValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado ao carregar EDF: {e}")

    # 3. Aplicar filtros
    if mode == "raw":
        message = "Dados crus carregados"
    elif mode == "standard":
        raw.filter(l_freq=1.0, h_freq=40.0)
        raw.notch_filter(freqs=50.0)
        message = "Filtro padrão aplicado (1-40Hz + notch 50Hz)"
    elif mode == "custom":
        if l_freq or h_freq:
            raw.filter(l_freq=l_freq, h_freq=h_freq)
        if notch:
            raw.notch_filter(freqs=notch)
        message = f"Filtro custom aplicado (l_freq={l_freq}, h_freq={h_freq}, notch={notch})"
    else:
        raise HTTPException(status_code=400, detail="Modo inválido")

    # 4. Criar pasta de saída
    output_dir = OUTPUT_CONTAINER_PATH / file_name.split('_')[0]
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{Path(file_name).stem}_filtered.fif"
    raw.save(output_path, overwrite=True)

    return {
        "message": message,
        "output_file": str(output_path),
        "n_channels": len(raw.ch_names),
        "duration_sec": raw.times[-1]
    }
