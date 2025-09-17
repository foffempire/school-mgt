from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from app.db.database import SessionDep
from app.db.models import Teacher
from .schema import TeacherCreate
from .services import get_teachers, create_teacher

router = APIRouter(prefix="/v1/_teacher", tags=["Admin Teachers"])

@router.get("/", response_model=List[Teacher])
def read_teachers(session: SessionDep):
    return get_teachers(session)

@router.post("/", response_model=Teacher)
def add_teacher(student: TeacherCreate, session: SessionDep) -> Teacher:
    return create_teacher(session, student)
