import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dicom_processor import extract_dicom_metadata

app = FastAPI(title="MedNAS DICOM Local API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STORAGE_PATH = os.getenv("STORAGE_PATH", "/data/dicom_inbound")

@app.get("/api/v1/scan")
def scan_dicom_files():
    """Escanea la carpeta de almacenamiento local del NAS y procesa los archivos .dcm"""
    results = []
    if not os.path.exists(STORAGE_PATH):
        return {"status": "success", "data": [], "message": f"Directorio {STORAGE_PATH} no montado aún."}

    for root, _, files in os.walk(STORAGE_PATH):
        for file in files:
            if file.lower().endswith(('.dcm', '.dicom')):
                full_path = os.path.join(root, file)
                metadata = extract_dicom_metadata(full_path)
                results.append(metadata)

    return {"status": "success", "count": len(results), "data": results}

# Servir interfaz web estática en la raíz
app.mount("/", StaticFiles(directory="../web", html=True), name="web")