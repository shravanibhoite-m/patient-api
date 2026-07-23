from fastapi import APIRouter, HTTPException, Body
from fastapi_pagination import Page, paginate
from typing import Optional
from patient_db import db_connection
from services import get_patient, get_all_patients, create_patient, updated_patient_resource, update_patient_record,delete_patient
from schemas import PatientCreate, PatientOut, PatientUpdate

router = APIRouter()
conn = db_connection()

@router.get("/patients/{patient_id}")
def get_patient_by_id(patient_id:int):
    patient=get_patient(conn,patient_id)
    if patient is None:
        raise HTTPException(status_code=404,detail="patient not found")
    return patient

@router.get("/patients",response_model=Page[PatientOut])
def get_patients():
    patients=get_all_patients(conn)
    return paginate(patients)


@router.post("/patients",status_code=201)
def insert_patient(patient:PatientCreate):
    result=create_patient(conn,patient.model_dump())
    return result
    
@router.put("/patients/{patient_id}")
def update_patient(patient_id:int,patient:PatientCreate):
    rows_affected=updated_patient_resource(conn,patient_id,patient)
    if rows_affected==0:
        raise HTTPException(status_code=404,detail="patient not found")
    return "patient updated successfully.."

@router.patch("/patients/{patient_id}")
def update_patient_field(
    patient_id: int,
    patient: Optional[PatientUpdate] = Body(default_factory=PatientUpdate)
):
    updated_data = patient.model_dump(exclude_unset=True)

    if not updated_data:
        raise HTTPException(status_code=400, detail="No fields provided")

    result = update_patient_record(conn, patient_id, updated_data)
    if result is None:
        raise HTTPException(status_code=404, detail="patient not found")
    return result

@router.delete("/patients/{patient_id}")
def delete_patient_by_id(patient_id:int):
    rows_affected=delete_patient(conn,patient_id)
    if rows_affected==0:
        raise HTTPException(status_code=404,detail="patient not found")
    return "patient deleted successfully.."