from typing import List, Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date, time, timezone
from enum import Enum
from app.db.models import School
from app.routes.admin.schema import AdminPublic
from app.routes.class_.schema import ClassPublic
from app.routes.class_arm.schema import ArmPublic
from app.routes.parent.schema import ParentPublic
from app.routes.staff.schema import StaffPublic
from app.routes.student.schema import StudentPublic
from app.routes.teacher.schema import TeacherPublic


class SchoolPublic(BaseModel):
    id: str
    name: str
    country: Optional[str]
    address: Optional[str]
    logo: Optional[str]
    referrer: Optional[str]
    is_active: Optional[bool]
    is_premium: Optional[bool]
    start_date: Optional[date]
    end_date: Optional[date]
    is_deleted: Optional[bool]
    date_deleted: Optional[date]
    date_created: date

    # staff: List[StaffPublic]
    # teacher: List[TeacherPublic]
    # student: List[StudentPublic]
    # parent: List[ParentPublic]
    # class_: List[ClassPublic]
    # arm: List[ArmPublic]
    # subject: List[SubjectPublic]
    # announcement: List[AnnouncementPublic]
    # events: List[EventsPublic]


class SchoolCreate(BaseModel):
    name: str
    address: Optional[str]
    country: Optional[str] = None
    referrer: Optional[str] = None


class SchoolUpdate(BaseModel):
    name: str
    country: Optional[str] = None
    address: Optional[str] = None


class SchoolLogo(BaseModel):
    logo: str

