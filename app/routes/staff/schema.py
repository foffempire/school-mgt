from typing import Optional
from pydantic import BaseModel
from datetime import date
from app.db.models import UserBase


class StaffPublic(UserBase):    
    staff_no: Optional[str] = None
    position: Optional[str] = None
    role: str
    hire_date: date
    qualification: Optional[str] = None
    nok_names: Optional[str] = None
    nok_address: Optional[str] = None
    nok_phone: Optional[str] = None
    nok_email: Optional[str] = None
    nok_relationship: Optional[str] = None




class StaffCreate(BaseModel):
    firstname: str
    lastname: str
    othername: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    gender: Optional[str]
    marital_status: str
    address: Optional[str]
    blood_group: Optional[str]
    Religion: Optional[str]
    bio: Optional[str] = None
    date_of_birth: Optional[date] = None
    image: Optional[str] = None
    staff_no: Optional[str] = None
    position: Optional[str] = None
    hire_date: date
    qualification: Optional[str] = None
    nok_names: Optional[str] = None
    nok_address: Optional[str] = None
    nok_phone: Optional[str] = None
    nok_email: Optional[str] = None
    nok_relationship: Optional[str] = None



class StaffUpdate(BaseModel):
    firstname: str
    lastname: str
    othername: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    gender: Optional[str]
    marital_status: str
    address: Optional[str]
    blood_group: Optional[str]
    Religion: Optional[str]
    bio: Optional[str] = None
    date_of_birth: Optional[date] = None
    staff_no: Optional[str] = None
    position: Optional[str] = None
    hire_date: date
    qualification: Optional[str] = None
    nok_names: Optional[str] = None
    nok_address: Optional[str] = None
    nok_phone: Optional[str] = None
    nok_email: Optional[str] = None
    nok_relationship: Optional[str] = None



