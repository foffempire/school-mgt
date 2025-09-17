from typing import List, Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date, time, timezone
from enum import Enum
from app.db.models import UserCreate, UserBase


class TeacherPublic(UserBase):    
    teacher_no: Optional[str] = None
    role: str
    hire_date: date
    qualification: Optional[str] = None
    nok_names: Optional[str] = None
    nok_address: Optional[str] = None
    nok_phone: Optional[str] = None
    nok_email: Optional[str] = None
    nok_relationship: Optional[str] = None



class TeacherCreate(UserCreate):    
    teacher_no: Optional[str] = None
    hire_date: date
    qualification: Optional[str] = None
    nok_names: Optional[str] = None
    nok_address: Optional[str] = None
    nok_phone: Optional[str] = None
    nok_email: Optional[str] = None
    nok_relationship: Optional[str] = None



class TeacherUpdate(BaseModel):
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
    teacher_no: Optional[str] = None
    hire_date: date
    qualification: Optional[str] = None
    nok_names: Optional[str] = None
    nok_address: Optional[str] = None
    nok_phone: Optional[str] = None
    nok_email: Optional[str] = None
    nok_relationship: Optional[str] = None
    bio: Optional[str]
    date_of_birth: Optional[date]