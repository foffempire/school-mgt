from fastapi import APIRouter, status
from typing import List
from app.db.database import SessionDep
from .schema import SchoolCreate, SchoolPublic, SchoolUpdate
from .services import create_school, delete_school, get_schools, get_school, update_school

router = APIRouter(prefix="/v1/_school", tags=["Admin Schools"])



@router.post("/", status_code=status.HTTP_200_OK, response_model=SchoolPublic)
def add_school(school: SchoolCreate, session: SessionDep):
    return create_school(session, school)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[SchoolPublic])
def read_schools(session: SessionDep):
    """Get all schools"""
    return get_schools(session)


@router.get("/{school_uid}", status_code=status.HTTP_200_OK, response_model=SchoolPublic)
def read_school(school_uid: str, session: SessionDep):
    """Get one school"""
    return get_school(school_uid, session)


@router.patch("/{school_uid}", status_code=status.HTTP_200_OK, response_model=SchoolPublic)
def edit_school(school_uid: str, school: SchoolUpdate, session: SessionDep):
    """Edit school"""
    return update_school(school_uid, school, session)


@router.patch("/delete/{school_uid}", status_code=status.HTTP_200_OK,)
def terminate_school(school_uid: str, session: SessionDep):
    """delete school"""
    return delete_school(school_uid, session)

