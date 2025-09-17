from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from app.db.database import SessionDep
from app.db.models import Student
from .schema import StudentCreate, StudentResponse
from app.core.utils import generate_unique_id
from .services import get_students, create_student

router = APIRouter(prefix="/v1/_student", tags=["Admin Students"])

@router.get("/", response_model=List[StudentResponse])
def read_students(session: SessionDep):
    return get_students(session)

@router.post("/", response_model=Student)
def add_student(student: StudentCreate, session: SessionDep) -> Student:
    return create_student(session, student)
