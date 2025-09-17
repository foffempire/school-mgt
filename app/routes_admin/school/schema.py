from typing import List, Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date, time, timezone
from enum import Enum
from app.db.models import School


class SchoolPublic(BaseModel):
    school_uid: str
    name: str
    address: str
    referrer: Optional[str]
    is_active: Optional[bool]
    is_premium: Optional[bool]
    start_date: Optional[date]
    end_date: Optional[date]
    is_deleted: Optional[bool]
    date_deleted: Optional[date]
    date_created: date



class SchoolCreate(BaseModel):
    name: str
    address: Optional[str] = None
    referrer: Optional[str] = None


class SchoolUpdate(BaseModel):
    name: str
    address: Optional[str] = None

