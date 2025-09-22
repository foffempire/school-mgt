from typing import Optional
from pydantic import BaseModel
from datetime import date
from app.routes.school.schema import SchoolPublic


class AuthUser(BaseModel):
    id: str
    # school_id: str
    firstname: Optional[str]
    lastname: Optional[str]
    email: Optional[str]
    role: Optional[str]
    is_active: Optional[bool]
    date_created: date
    school: Optional[SchoolPublic]



class AuthPublic(BaseModel):
    access_token: str
    token_type: str
    user: AuthUser