from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date, time, timezone
from enum import Enum
from app.db.models import Class_, Parent, UserBase, UserCreate, Student
from app.routes.class_arm.schema import ArmPublic
from app.routes.parent.schema import ParentPublic

class StudentPublic(UserBase):
    student_no: Optional[str] = None
    enrollment_date: date
    class_id: Optional[int] = None
    arm_id: Optional[int] = None
    parent_id: Optional[int] = None
    
    arm: Optional[ArmPublic]
    parent: Optional[ParentPublic] = None



class StudentCreate(UserCreate):    
    student_no: Optional[str] = None
    enrollment_date: date
    class_id: Optional[int] = None
    parent_id: Optional[int] = None


