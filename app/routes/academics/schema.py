from typing import Optional
from pydantic import BaseModel
from datetime import date


# class SessionPublic(AcademicSession):
#     pass



class SessionCreate(BaseModel):
    name: str
    current: Optional[bool] = False







