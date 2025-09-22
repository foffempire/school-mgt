from fastapi import APIRouter
from typing import List
from app.db.database import SessionDep
from app.security.oauth2 import CurrentUserDep
from .schema import ArmCreate, ArmPublic
from .services import deactivate_arm, get_arm, get_arms, create_arm, update_arm

router = APIRouter(prefix="/v1/arm", tags=["Arm"])

@router.post("/")
def add_arm(school_arm: List[ArmCreate], current_admin: CurrentUserDep, db: SessionDep):
    return create_arm(current_admin.school_id, db, school_arm)


@router.get("/", response_model=List[ArmPublic])
def read_arms(db: SessionDep, current_admin: CurrentUserDep):
    return get_arms( current_admin.school_id, db)


@router.get("/{id}", response_model=ArmPublic)
def read_arm(id: str, db: SessionDep, current_admin: CurrentUserDep):
    return get_arm(id, current_admin.school_id, db)


@router.patch("/{id}", response_model=ArmPublic)
def edit_arm(id: str, school_arm: ArmCreate, db: SessionDep, current_admin: CurrentUserDep):
    return update_arm(id, current_admin.school_id, school_arm, db)


@router.patch("/delete/{id}")
def delete_arm(id: str, db: SessionDep, current_admin: CurrentUserDep):
    return deactivate_arm(id, current_admin.school_id, db)
