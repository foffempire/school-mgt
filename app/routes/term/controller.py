from fastapi import APIRouter, Depends
from typing import List
from app.db.database import SessionDep
from app.db.models import Term
from app.security.oauth2 import CurrentUserDep
from .schema import TermCreate
from .services import edit_term, get_term, get_terms, create_term

router = APIRouter(prefix="/v1/term", tags=["Term"])

@router.get("/", response_model=List[Term])
def read_terms(current_user: CurrentUserDep, db: SessionDep):
    return get_terms(current_user.school_id, db)



@router.get("/{term_id}", response_model=Term)
def read_term(term_id, current_user: CurrentUserDep, db: SessionDep):
    return get_term(term_id, current_user.school_id, db)



@router.post("/", response_model=Term)
def add_term(current_user: CurrentUserDep, student: TermCreate, db: SessionDep):
    return create_term(current_user.school_id, db, student)



@router.patch("/{term_id}", response_model=Term)
def update_term(term_id, current_user: CurrentUserDep, student: TermCreate, db: SessionDep):
    return edit_term(term_id, current_user.school_id, db, student)


