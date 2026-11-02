import os
import pydicom
from typing import Dict, Any

def extract_dicom_metadata(file_path: str) -> Dict[str, Any]:
    """Extrae metadatos DICOM clave usando pydicom."""
    try:
        ds = pydicom.dcmread(file_path, stop_before_pixels=True)
        return {
            "patient_id": getattr(ds, "PatientID", "ANONYMOUS"),
            "study_date": getattr(ds, "StudyDate", "Desconocida"),
            "modality": getattr(ds, "Modality", "UNKNOWN"),
            "study_description": getattr(ds, "StudyDescription", "Sin descripción"),
            "body_part_examined": getattr(ds, "BodyPartExamined", "N/A"),
            "institution_name": getattr(ds, "InstitutionName", "Local Clinic"),
            "file_name": os.path.basename(file_path)
        }
    except Exception as e:
        return {"error": f"Error al procesar el archivo DICOM: {str(e)}"}