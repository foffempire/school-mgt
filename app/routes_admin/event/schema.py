from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date, time, timezone
from enum import Enum
from app.db.models import Role


class ClassCreate(SQLModel):
    name: str
    room_number: Optional[str]
    academic_year: Optional[str]