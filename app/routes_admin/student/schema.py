from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date, time, timezone
from enum import Enum
from app.db.models import Class_, Parent, Role, UserCreate, Student


class StudentCreate(UserCreate):    
    student_no: Optional[str] = None
    enrollment_date: date
    class_id: Optional[int] = None
    parent_id: Optional[int] = None


class StudentResponse(StudentCreate):
    class_: Class_ | None
    parent: Parent | None