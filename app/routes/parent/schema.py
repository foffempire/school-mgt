from typing import List, Optional
from pydantic import BaseModel
from datetime import date 
from app.db.models import UserBase
from app.routes.student.schema import StudentPublic


class ParentPublic(UserBase):    
    occupation: Optional[str] = None
    role: str
    students: List[StudentPublic]=[]


class ParentCreate(BaseModel):
    firstname: str
    lastname: str
    othername: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    gender: Optional[str]
    marital_status: str
    address: Optional[str]
    blood_group: Optional[str]
    religion: Optional[str]
    bio: Optional[str] = None
    image: Optional[str] = None
    date_of_birth: Optional[date] = None
    occupation: Optional[str] = None



class ParentUpdate(BaseModel):
    firstname: str
    lastname: str
    othername: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    gender: Optional[str]
    marital_status: str
    address: Optional[str]
    blood_group: Optional[str]
    religion: Optional[str]
    bio: Optional[str]
    date_of_birth: Optional[date]
    occupation: Optional[str] = None



