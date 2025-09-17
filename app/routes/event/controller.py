from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from app.db.database import SessionDep
from app.db.models import Class
from .schema import ClassCreate
from app.core.utils import generate_unique_id
from .services import get_classes, create_class

router = APIRouter(prefix="/v1/class", tags=["Classes"])

@router.get("/", response_model=List[Class])
def read_classes(session: SessionDep):
    return get_classes(session)

@router.post("/", response_model=Class)
def add_class(student: ClassCreate, session: SessionDep) -> Class:
    return create_class(session, student)
