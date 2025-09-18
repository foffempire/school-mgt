from fastapi import APIRouter
from typing import List
from app.db.database import SessionDep
from app.security.oauth2 import CurrentUserDep
from .schema import ParentCreate, ParentPublic, ParentUpdate
from .services import deactivate_parent, edit_parent, get_parent, get_parents, create_parent

router = APIRouter(prefix="/v1/parent", tags=["Parents"])

@router.get("/", response_model=List[ParentPublic])
def read_parents(current_user: CurrentUserDep, db: SessionDep):
    return get_parents(current_user.school_id, db)


@router.get("/{parent_id}", response_model=ParentPublic)
def read_parent(parent_id, current_user: CurrentUserDep, db: SessionDep):
    return get_parent(parent_id, current_user.school_id, db)



@router.post("/", response_model=ParentPublic)
def add_parent(current_user: CurrentUserDep, parent: ParentCreate, db: SessionDep):
    return create_parent(current_user.school_id, db, parent)


@router.patch("/{parent_id}", response_model=ParentPublic)
def update_parent(parent_id, current_user: CurrentUserDep, parent: ParentUpdate, db: SessionDep):
    return edit_parent(parent_id, current_user.school_id, db, parent)



@router.patch("/delete/{parent_id}")
def delete_parent(parent_id, current_user: CurrentUserDep, db: SessionDep):
    return deactivate_parent(parent_id, current_user.school_id, db)