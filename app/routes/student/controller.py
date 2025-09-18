from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from app.db.database import SessionDep
from app.db.models import Student
from app.security.oauth2 import CurrentUserDep
from .schema import StudentCreate, StudentPublic, StudentUpdate
from .services import archive_student, deactivate_student, edit_student, get_archived_students, get_student, get_students, create_student

router = APIRouter(prefix="/v1/student", tags=["Students"])

@router.get("/", response_model=List[StudentPublic])
def read_students(current_user: CurrentUserDep, db: SessionDep):
    return get_students(current_user.school_id, db)



@router.get("/{student_id}", response_model=StudentPublic)
def read_student(student_id, current_user: CurrentUserDep, db: SessionDep):
    return get_student(student_id, current_user.school_id, db)



@router.post("/", response_model=StudentPublic)
def add_student(current_user: CurrentUserDep, student: StudentCreate, db: SessionDep):
    return create_student(current_user.school_id, db, student)



@router.patch("/{student_id}", response_model=StudentPublic)
def update_student(student_id, current_user: CurrentUserDep, student: StudentUpdate, db: SessionDep):
    return edit_student(student_id, current_user.school_id, db, student)



@router.patch("/archive/{student_id}")
def archive_a_student(student_id, current_user: CurrentUserDep, db: SessionDep):
    return archive_student(student_id, current_user.school_id, db)



@router.get("/archived", response_model=List[StudentPublic])
def archived_students(current_user: CurrentUserDep, db: SessionDep):
    return get_archived_students(current_user.school_id, db)



@router.patch("/delete/{student_id}")
def delete_student(student_id, current_user: CurrentUserDep, db: SessionDep):
    return deactivate_student(student_id, current_user.school_id, db)