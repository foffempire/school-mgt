from typing import List, Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date, time, timezone
from enum import Enum
from app.db.models import Role, School


class AuthUser(BaseModel):
    id: str
    school_id: str
    firstname: Optional[str]
    lastname: Optional[str]
    email: Optional[str]
    role: Optional[str]
    is_active: Optional[bool]
    date_created: date



class AuthPublic(BaseModel):
    access_token: str
    token_type: str
    user: AuthUser