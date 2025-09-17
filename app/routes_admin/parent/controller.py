from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from app.db.database import SessionDep
from app.db.models import Parent
from .schema import ParentCreate, ParentResponse
from app.core.utils import generate_unique_id
from .services import get_parents, create_parent

router = APIRouter(prefix="/v1/_parent", tags=["Admin Parents"])

@router.get("/", response_model=List[ParentResponse])
def read_parents(session: SessionDep):
    return get_parents(session)

@router.post("/", response_model=Parent)
def add_parent(student: ParentCreate, session: SessionDep) -> Parent:
    return create_parent(session, student)
