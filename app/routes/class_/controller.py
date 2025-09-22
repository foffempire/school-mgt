from fastapi import APIRouter
from typing import List
from app.db.database import SessionDep
from app.security.oauth2 import CurrentUserDep
from .schema import ClassCreate, ClassPublic
from .services import deactivate_class, get_class, get_classes, create_class, update_class

router = APIRouter(prefix="/v1/class", tags=["Classes"])

@router.post("/")
def add_class(school_class: List[ClassCreate], current_admin: CurrentUserDep, db: SessionDep):
    return create_class(current_admin.school_id, db, school_class)


@router.get("/", response_model=List[ClassPublic])
def read_classes(db: SessionDep, current_admin: CurrentUserDep):
    return get_classes( current_admin.school_id, db)


@router.get("/{id}", response_model=ClassPublic)
def read_class(id: str, db: SessionDep, current_admin: CurrentUserDep):
    return get_class(id, current_admin.school_id, db)


@router.patch("/{id}", response_model=ClassPublic)
def edit_class(id: str, school_class: ClassCreate, db: SessionDep, current_admin: CurrentUserDep):
    return update_class(id, current_admin.school_id, school_class, db)


@router.patch("/delete/{id}")
def delete_class(id: str, db: SessionDep, current_admin: CurrentUserDep):
    return deactivate_class(id, current_admin.school_id, db)
