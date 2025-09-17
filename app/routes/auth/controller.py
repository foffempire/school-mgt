from fastapi import APIRouter, Depends
from typing import List

from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import SessionDep
from .services import login_
from .schema import AuthPublic


router = APIRouter(prefix="/v1/auth", tags=["Authentication"])

@router.post("/", response_model=AuthPublic)
async def login(db: SessionDep,  form_data: OAuth2PasswordRequestForm = Depends()):
    return await login_(db, form_data)

