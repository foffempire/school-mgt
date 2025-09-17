from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date, time, timezone
from enum import Enum
from app.db.models import Role


class ArmPublic(SQLModel):
    id: str
    school_id: str
    name: str
    is_active: bool


class ArmCreate(SQLModel):
    name: str

