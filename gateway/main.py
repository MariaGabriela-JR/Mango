from fastapi import FastAPI
from routers.scientists_route import router as scientists_router
from routers.patients_route import router as patients_router
from routers.edf_files_route import router as edf_files_router
from routers.filters_route import router as filters_router

app = FastAPI(
    title="Medical Data Processing API",
    description="API Gateway for scientists, patients and EDF Files",
    version="1.0.0"
)

# ================================
# REGISTER ROUTERS
# ================================
app.include_router(scientists_router, prefix="/api/scientists")
app.include_router(patients_router, prefix="/api/patients")
app.include_router(edf_files_router, prefix="/api/edf_files")
app.include_router(filters_router, prefix="/api/filters")
# ================================
# HEALTHCHECK / ROOT
# ================================
@app.get("/")
async def root():
    return {"status": "ok", "message": "API Gateway running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
