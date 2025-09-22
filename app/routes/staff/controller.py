from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from app.db.database import SessionDep
from app.db.models import Staff
from app.security.oauth2 import CurrentUserDep
from .schema import StaffCreate, StaffPublic, StaffUpdate
from .services import archive_staff, deactivate_staff, edit_staff, get_archived_staffs, get_staff, get_staffs, create_staff

router = APIRouter(prefix="/v1/staff", tags=["Staff"])

@router.get("/", response_model=List[StaffPublic])
def read_staffs(current_user: CurrentUserDep, db: SessionDep):
    return get_staffs(current_user.school_id, db)


@router.get("/{staff_id}", response_model=StaffPublic)
def read_staff(staff_id, current_user: CurrentUserDep, db: SessionDep):
    return get_staff(staff_id, current_user.school_id, db)



@router.post("/", response_model=StaffPublic)
def add_staff(current_user: CurrentUserDep, staff: StaffCreate, db: SessionDep):
    return create_staff(current_user.school_id, db, staff)


@router.patch("/{staff_id}", response_model=StaffPublic)
def update_staff(staff_id, current_user: CurrentUserDep, staff: StaffUpdate, db: SessionDep):
    return edit_staff(staff_id, current_user.school_id, db, staff)



@router.get("/archive/all", response_model=List[StaffPublic])
def archived_staffs(current_user: CurrentUserDep, db: SessionDep):
    return get_archived_staffs(current_user.school_id, db)



@router.patch("/archive/{staff_id}")
def archive_a_staff(staff_id, current_user: CurrentUserDep, db: SessionDep):
    return archive_staff(staff_id, current_user.school_id, db)



@router.patch("/delete/{staff_id}")
def delete_staff(staff_id, current_user: CurrentUserDep, db: SessionDep):
    return deactivate_staff(staff_id, current_user.school_id, db)