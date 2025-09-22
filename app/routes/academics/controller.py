from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from app.db.database import SessionDep
from app.db.models import AcademicSession
from app.security.oauth2 import CurrentUserDep
from .schema import SessionCreate
from .services import deactivate_academic_session, edit_academic_session, get_academic_session, get_academic_sessions, create_academic_session

router = APIRouter(prefix="/v1/academicsession", tags=["Academic Session"])

@router.get("/", response_model=List[AcademicSession])
def read_academic_sessions(current_user: CurrentUserDep, db: SessionDep):
    return get_academic_sessions(current_user.school_id, db)



@router.get("/{year_id}", response_model=AcademicSession)
def read_academic_session(year_id, current_user: CurrentUserDep, db: SessionDep):
    return get_academic_session(year_id, current_user.school_id, db)



@router.post("/", response_model=AcademicSession)
def add_academic_session(current_user: CurrentUserDep, student: SessionCreate, db: SessionDep):
    return create_academic_session(current_user.school_id, db, student)



@router.patch("/{year_id}", response_model=AcademicSession)
def update_academic_session(year_id, current_user: CurrentUserDep, student: SessionCreate, db: SessionDep):
    return edit_academic_session(year_id, current_user.school_id, db, student)



@router.patch("/delete/{year_id}")
def delete_academic_session(year_id, current_user: CurrentUserDep, db: SessionDep):
    return deactivate_academic_session(year_id, current_user.school_id, db)