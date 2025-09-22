from typing import Optional
from pydantic import BaseModel
from datetime import date


# class TermPublic(AcademicTerm):
#     pass



class TermCreate(BaseModel):
    name: str
    start_date: date
    end_date: date







