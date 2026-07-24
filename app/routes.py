from fastapi import APIRouter, HTTPException, Body
from fastapi_pagination import Page, paginate
from typing import Optional
from db import db_connection
from services import get_patient, get_all_patients, create_patient, updated_patient_resource, update_patient_record,delete_patient
from schemas import PatientCreate, PatientOut, PatientUpdate
from argon2 import PasswordHasher
from logger import logger
ph = PasswordHasher()

router = APIRouter()
conn = db_connection()

@router.get("/patients/{patient_id}", response_model=PatientOut)
def get_patient_by_id(patient_id:int):
    patient=get_patient(conn,patient_id)
    if patient is None:
        logger.error(f"Patient with ID {patient_id} not found.")
        raise HTTPException(status_code=404,detail="patient not found")
    logger.info(f"Patient with ID {patient_id} retrieved successfully.")
    return patient

@router.get("/patients",response_model=Page[PatientOut])
def get_patients():
    patients=get_all_patients(conn)
    logger.info(f"Retrieved {len(patients)} patients from the database.")
    return paginate(patients)


@router.post("/patients",status_code=201,response_model=PatientOut)
def insert_patient(patient:PatientCreate):
    patient_data = patient.model_dump()
    patient_data["password"] = ph.hash(patient_data["password"])
    result=create_patient(conn,patient_data)
    logger.info(f"Patient created successfully with ID {result['id']}.")
    return result
    
@router.put("/patients/{patient_id}",response_model=PatientOut)
def update_patient(patient_id:int,patient:PatientCreate):
    try:
        patient_data = patient.model_dump()
        patient_data["password"] = ph.hash(patient_data["password"])
        rows_affected=updated_patient_resource(conn,patient_id,patient_data)
        if rows_affected==0:
            logger.error(f"Patient with ID {patient_id} not found.")
            raise HTTPException(status_code=404,detail="patient not found")
        logger.info(f"Patient with ID {patient_id} record updated successfully.")
        return get_patient(conn, patient_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating patient with ID {patient_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.patch("/patients/{patient_id}",response_model=PatientOut)
def update_patient_field(
    patient_id: int,
    patient: Optional[PatientUpdate] = Body(default_factory=PatientUpdate)
):
    updated_data = patient.model_dump(exclude_unset=True)

    if not updated_data:
        logger.error(f"No fields provided for update for patient ID {patient_id}.")
        raise HTTPException(status_code=400, detail="No fields provided")

    result = update_patient_record(conn, patient_id, updated_data)
    if result is None:
        logger.error(f"Patient with ID {patient_id} not found.")
        raise HTTPException(status_code=404, detail="patient not found")
    logger.info(f"Patient with ID {patient_id} updated successfully.")
    return result

@router.delete("/patients/{patient_id}")
def delete_patient_by_id(patient_id:int):
    rows_affected=delete_patient(conn,patient_id)
    if rows_affected==0:
        logger.error(f"Patient with ID {patient_id} not found.")
        raise HTTPException(status_code=404,detail="patient not found")
    logger.info(f"Patient with ID {patient_id} deleted successfully.")
    return "patient deleted successfully.."