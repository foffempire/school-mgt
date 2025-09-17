from typing import List, Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date, time, timezone
from enum import Enum
from app.db.models import Role, School


class AdminPublic(BaseModel):
    id: str
    school_id: str
    firstname: Optional[str]
    lastname: Optional[str]
    email: Optional[str]
    role: Optional[str]
    is_active: Optional[bool]


class AdminCreateResponse(BaseModel):
    access_token: str
    token_type: str
    user: AdminPublic


class AdminCreate(BaseModel):
    school_id: str
    email: str
    password: str
    firstname: Optional[str] = None
    lastname: Optional[str] = None


class MakeAdmin(BaseModel):
    email: str
    password: str
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    role: Role = 'staff'


class AdminUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None


class AdminPassword(BaseModel):
    current_password: str
    new_password: str


