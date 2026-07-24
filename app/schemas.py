from pydantic import BaseModel,Field,EmailStr
from enum import Enum
from typing import Optional

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

class PatientUpdate(BaseModel):
     name:Optional[str]=None
     age:Optional[int]=Field(default=None,ge=0,le=150)
     email:Optional[EmailStr]=None
     phone_num:Optional[str]=None
     active:Optional[bool]=None
     blood_group:Optional[Bloodgroup]=None
     emergency_contact:Optional[str]=None
     city:Optional[str]=None
     pincode:Optional[int]=Field(default=None,ge=100000,le=999999)
