from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date, time, timezone
from enum import Enum
from app.db.models import Role, UserCreate


class TeacherCreate(UserCreate):    
    teacher_no: Optional[str] = None
    marital_statue: str
    hire_date: date
    qualification: Optional[str] = None
    nok_names: Optional[str] = None
    nok_address: Optional[str] = None
    nok_phone: Optional[str] = None
    nok_email: Optional[str] = None
    nok_relationsip: Optional[str] = None