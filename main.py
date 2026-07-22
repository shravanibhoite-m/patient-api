from patient_db import db_connection
from services import get_patient,get_all_patients,create_patient,updated_patient_resource
from pydantic import BaseModel,Field,field_validator,EmailStr
from fastapi import FastAPI,HTTPException
from enum import Enum
from typing import Optional
from fastapi_pagination import Page, add_pagination, paginate
from dotenv import load_dotenv
load_dotenv()


app=FastAPI()
conn=db_connection()



class Bloodgroup(str,Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    O_POS = "O+"
    O_NEG = "O-"
    AB_POS = "AB+"
    AB_NEG = "AB-"

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class PatientOut(BaseModel):
    id: int=Field(ge=0,le=100)

    name: str
    age: int=Field(ge=0,le=150)
    gender: Gender
    email: EmailStr
    phone_num:Optional[str]=None
    active: bool=True
    blood_group:Bloodgroup
    emergency_contact: str
    city: str
    pincode: int=Field(ge=100000,le=999999)

class PatientCreate(BaseModel):
    name: str
    age: int=Field(ge=0,le=150)
    gender: Gender
    email: EmailStr
    phone_num:Optional[str]=None
    password:str
    active: bool=True
    blood_group:Bloodgroup
    emergency_contact: str
    city: str
    pincode: int=Field(ge=100000,le=999999)

@app.get("/patients/{patient_id}")
def get_patient_by_id(patient_id:int):
    patient=get_patient(conn,patient_id)
    if patient_id is None:
        raise HTTPException(status_code=404,detail="patient not found")
    return patient

@app.get("/patients",response_model=Page[PatientOut])
def get_patients():
    patients=get_all_patients(conn)
    return paginate(patients)
add_pagination(app)

@app.post("/patients",status_code=201)
def insert_patient(patient:PatientCreate):
    create_patient(conn,patient.model_dump())
    
@app.put("/patients/{patient_id}")
def update_patient(patient_id:int,patient:PatientCreate):
    rows_affected=updated_patient_resource(conn,patient_id,patient)
    if rows_affected==0:
        raise HTTPException(status_code=404,detail="patient not found")
    return "patient updated successfully.."
    
    