from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from app.db.database import SessionDep
from app.db.models import Teacher
from app.security.oauth2 import CurrentUserDep
from .schema import TeacherCreate, TeacherUpdate
from .services import deactivate_teacher, edit_teacher, get_teachers, create_teacher

router = APIRouter(prefix="/v1/teacher", tags=["Teachers"])

@router.get("/", response_model=List[Teacher])
def read_teachers(current_user: CurrentUserDep, db: SessionDep):
    return get_teachers(current_user.school_id, db)



@router.post("/", response_model=Teacher)
def add_teacher(current_user: CurrentUserDep, teacher: TeacherUpdate, db: SessionDep):
    return create_teacher(current_user.school_id, db, teacher)


@router.patch("/{id}", response_model=Teacher)
def update_teacher(id, current_user: CurrentUserDep, teacher: TeacherUpdate, db: SessionDep):
    return edit_teacher(id, current_user.school_id, db, teacher)



@router.patch("/delete/{id}")
def delete_teacher(id, current_user: CurrentUserDep, db: SessionDep):
    return deactivate_teacher(id, current_user.school_id, db)