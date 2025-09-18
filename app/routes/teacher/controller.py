from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from app.db.database import SessionDep
from app.db.models import Teacher
from app.security.oauth2 import CurrentUserDep
from .schema import TeacherCreate, TeacherPublic, TeacherUpdate
from .services import deactivate_teacher, edit_teacher, get_teacher, get_teachers, create_teacher

router = APIRouter(prefix="/v1/teacher", tags=["Teachers"])

@router.get("/", response_model=List[TeacherPublic])
def read_teachers(current_user: CurrentUserDep, db: SessionDep):
    return get_teachers(current_user.school_id, db)


@router.get("/{teacher_id}", response_model=TeacherPublic)
def read_teacher(teacher_id, current_user: CurrentUserDep, db: SessionDep):
    return get_teacher(teacher_id, current_user.school_id, db)



@router.post("/", response_model=TeacherPublic)
def add_teacher(current_user: CurrentUserDep, teacher: TeacherCreate, db: SessionDep):
    return create_teacher(current_user.school_id, db, teacher)


@router.patch("/{teacher_id}", response_model=TeacherPublic)
def update_teacher(teacher_id, current_user: CurrentUserDep, teacher: TeacherUpdate, db: SessionDep):
    return edit_teacher(teacher_id, current_user.school_id, db, teacher)



@router.patch("/delete/{teacher_id}")
def delete_teacher(teacher_id, current_user: CurrentUserDep, db: SessionDep):
    return deactivate_teacher(teacher_id, current_user.school_id, db)