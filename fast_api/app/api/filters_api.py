import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.filters import filter_data
from app.core.dependencies import discover_files, load_and_validate_file
from app.core.database import get_db
from app.core.models import EDFFile, PatientMetadata, Trial

router = APIRouter()

OUTPUT_CONTAINER_PATH = Path(os.getenv("OUTPUT_CONTAINER_PATH", "/tmp/output"))

# ---------- HELPERS ----------
def process_and_save(
    file_name: str,
    raw,
    mode: str,
    db: Session,
    patient_metadata: dict | None = None,
    trial_metadata: dict | None = None,
    config: dict | None = None,
):
    raw_filtered = filter_data(
        raw,
        mode=mode,
        patient_metadata=patient_metadata,
        trial_metadata=trial_metadata,
        config=config,
    )

    # Pasta de saída
    output_dir = OUTPUT_CONTAINER_PATH / file_name.split("_")[0]
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{Path(file_name).stem}_filtered.fif"
    raw_filtered.save(output_path, overwrite=True)

    # Atualiza status na DB
    db_file = db.query(EDFFile).filter(EDFFile.file_name == file_name).first()
    if db_file:
        db_file.processing_status = "filtered"
        db.commit()
        db.refresh(db_file)

    return str(output_path), len(raw_filtered.ch_names), raw_filtered.times[-1]


# ---------- ROUTES ----------
@router.get("/discover")
def discover():
    return discover_files()


@router.post("/{file_name}/apply")
def apply_filters(
    file_name: str,
    background_tasks: BackgroundTasks,
    mode: str = Query("standard", enum=["standard", "auto", "custom"]),
    l_freq: float | None = Query(None, description="Passa-alta (custom)"),
    h_freq: float | None = Query(None, description="Passa-baixa (custom)"),
    notch: float | None = Query(None, description="Notch (custom)"),
    patient_id: str | None = Query(None, description="patient_iid (auto)"),
    trial_id: str | None = Query(None, description="ID do trial (auto)"),
    db: Session = Depends(get_db),
):
    # Carrega e valida EDF
    raw, file_path = load_and_validate_file(file_name)

    patient_metadata = None
    trial_metadata = None
    config = None

    # ---------- STANDARD ----------
    if mode == "standard":
        pass  # Não precisa de config/metadados

    # ---------- AUTO ----------
    elif mode == "auto":
        if not patient_id:
            raise HTTPException(status_code=400, detail="É necessário fornecer patient_id para filtro automático.")

        patient = db.query(PatientMetadata).filter(PatientMetadata.patient_iid == patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail=f"Paciente {patient_id} não encontrado na base de dados.")

        patient_metadata = {
            "age": patient.age,
            "gender": patient.gender,
            "clinical_notes": patient.clinical_notes,
            "additional_info": patient.additional_info,
        }

        if trial_id:
            trial = db.query(Trial).filter(Trial.id == trial_id).first()
            if not trial:
                raise HTTPException(status_code=404, detail=f"Trial {trial_id} não encontrado na base de dados.")

            trial_metadata = {
                "trial_index": trial.trial_index,
                "start_time": trial.start_time,
                "duration": trial.duration,
                "emotion_category": trial.emotion_category,
                "description": trial.description,
                "parameters": trial.parameters,
            }

    # ---------- CUSTOM ----------
    elif mode == "custom":
        config = {}
        if l_freq:
            config["highpass"] = l_freq
        if h_freq:
            config["lowpass"] = h_freq
        if notch:
            config["notch"] = [notch]

    else:
        raise HTTPException(status_code=400, detail="Modo inválido")

    # ---------- EXECUTA EM BACKGROUND ----------
    background_tasks.add_task(
        process_and_save,
        file_name=file_name,
        raw=raw,
        mode=mode,
        db=db,
        patient_metadata=patient_metadata,
        trial_metadata=trial_metadata,
        config=config,
    )

    return {
        "message": f"Filtro iniciado em background → file_name={file_name}, mode={mode}",
        "output_dir": str(OUTPUT_CONTAINER_PATH / file_name.split("_")[0]),
    }
