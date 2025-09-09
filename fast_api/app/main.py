from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import edf_files, patient_metadata, trials, auth

# Lifespan para conexões
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializações
    yield

app = FastAPI(
    title="EDF Files API",
    description="API para gerenciamento de arquivos EDF e dados de pacientes",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(edf_files.router, prefix="/api/edf-files", tags=["EDF Files"])
app.include_router(patient_metadata.router, prefix="/api/patients", tags=["Patients"])
app.include_router(trials.router, prefix="/api/trials", tags=["Trials"])

# Endpoints 
@app.get("/")
async def root():
    return {"message": "Raiz do FastAPI!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
