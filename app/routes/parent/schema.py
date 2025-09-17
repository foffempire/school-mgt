from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date, time, timezone
from enum import Enum
from app.db.models import UserBase, Student, UserCreate


class ParentPublic(UserBase):
    pass


class ParentCreate(UserCreate):
    occupation: Optional[str] = None

