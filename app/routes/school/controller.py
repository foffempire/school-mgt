from fastapi import APIRouter, status
from typing import List
from app.db.database import SessionDep
from app.security.oauth2 import AdminUserDep, CurrentUserDep
from .schema import SchoolCreate, SchoolPublic, SchoolUpdate
from .services import create_school, delete_school, get_school, school_info, update_school

router = APIRouter(prefix="/v1/school", tags=["Schools"])



@router.post("/", status_code=status.HTTP_200_OK, response_model=SchoolPublic)
def add_school(school: SchoolCreate, session: SessionDep):
    return create_school(session, school)


@router.get("/complete", status_code=status.HTTP_200_OK)
def my_school_info(session: SessionDep, current_admin: CurrentUserDep):
    """Get complete school INFO"""
    return school_info(current_admin.school_id, session)


@router.get("/", status_code=status.HTTP_200_OK, response_model=SchoolPublic)
def my_school(session: SessionDep, current_admin: CurrentUserDep):
    """Get my school details"""
    return get_school(current_admin.school_id, session)


@router.patch("/", status_code=status.HTTP_200_OK, response_model=SchoolPublic)
def edit_school(school: SchoolUpdate, session: SessionDep, current_admin: CurrentUserDep):
    """Edit school"""
    return update_school(current_admin.school_id, school, session)


@router.patch("/delete", status_code=status.HTTP_200_OK,)
def terminate_school(session: SessionDep, current_admin: CurrentUserDep):
    """delete school"""
    return delete_school(current_admin.school_id, session)

