from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date, time, timezone
from enum import Enum
from app.db.models import Role


class ClassPublic(SQLModel):
    id: str
    school_id: str
    name: str
    is_active: bool
    room_number: Optional[str] = None
    academic_year: Optional[str] = None


class ClassCreate(SQLModel):
    name: str

