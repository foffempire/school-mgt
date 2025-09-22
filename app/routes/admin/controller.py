from fastapi import APIRouter, status
from typing import List
from app.db.database import SessionDep
from app.security.oauth2 import AdminUserDep
from .schema import AdminCreate, AdminPublic, MakeAdmin, AdminCreateResponse
from .services import create_account, deactivate_account, make_admin, me_account

router = APIRouter(prefix="/v1/admin", tags=["Admin"])



@router.post("/", status_code=status.HTTP_200_OK, response_model=AdminCreateResponse)
def add_account(admin: AdminCreate, db: SessionDep):
    return create_account(db, admin)


@router.post("/new", status_code=status.HTTP_200_OK, response_model=AdminPublic)
def make_account(new: MakeAdmin, db: SessionDep, current_admin: AdminUserDep):
    return make_admin(db, current_admin.school_id, new)


@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
def delete_account(user_id, db: SessionDep, current_admin: AdminUserDep):
    return deactivate_account(user_id, db)



@router.get("/me", status_code=status.HTTP_200_OK, response_model=AdminPublic)
def my_account(db: SessionDep, current_admin: AdminUserDep):
    return me_account(current_admin.id, db)

# @router.get("/", status_code=status.HTTP_200_OK, response_model=List[SchoolPublic])
# def read_schools(session: SessionDep):
#     """Get all schools"""
#     return get_schools(session)


# @router.get("/{id}", status_code=status.HTTP_200_OK, response_model=SchoolPublic)
# def read_school(id: str, session: SessionDep):
#     """Get one school"""
#     return get_school(id, session)


# @router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=SchoolPublic)
# def edit_school(id: str, school: SchoolUpdate, session: SessionDep):
#     """Edit school"""
#     return update_school(id, school, session)


# @router.patch("/delete/{id}", status_code=status.HTTP_200_OK,)
# def terminate_school(id: str, session: SessionDep):
#     """delete school"""
#     return delete_school(id, session)

