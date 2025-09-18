from typing import Optional
from pydantic import BaseModel
from datetime import date
from enum import Enum
from app.db.models import Parent, UserBase
from app.routes.class_.schema import ClassPublic
from app.routes.class_arm.schema import ArmPublic


class StudentPublic(UserBase):    
    role: str
    student_no: Optional[str] = None
    enrollment_date: date
    # class_id: Optional[str] = None
    # arm_id: Optional[str] = None
    # parent_id: Optional[str] = None

    class_: Optional[ClassPublic] = []
    arm: Optional[ArmPublic] = []
    parent: Optional[Parent] = []



class StudentCreate(BaseModel):
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
    image: Optional[str] = None
    date_of_birth: Optional[date] = None
    student_no: Optional[str] = None
    enrollment_date: date
    class_id: Optional[str] = None
    arm_id: Optional[str] = None
    parent_id: Optional[str] = None



class StudentUpdate(BaseModel):
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
    bio: Optional[str]
    date_of_birth: Optional[date]
    student_no: Optional[str] = None
    enrollment_date: date
    class_id: Optional[str] = None
    arm_id: Optional[str] = None
    parent_id: Optional[str] = None



