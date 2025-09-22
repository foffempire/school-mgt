from fastapi import HTTPException, status
from sqlmodel import Session, select
from app.db.models import Term
from .schema import TermCreate


def term_exist(school_id, name, db: Session):
    stmt = db.exec(select(Term).where(Term.name == name, Term.school_id == school_id)).first()
    if stmt:
        return True
    else:
        return False



def create_term(school_id, db: Session, data: TermCreate):

    if(term_exist(school_id, data.name, db )):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You already created this term.")
    

    sid = {"school_id": school_id}
    query = Term.model_validate(data.model_dump() | sid)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def get_terms(school_id, db: Session):
    return db.exec(select(Term).where(Term.school_id == school_id)).all()



def get_term(term_id, school_id, db: Session):
    query = db.exec(select(Term).where(Term.school_id == school_id, Term.id == term_id)).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    return query



def edit_term(id, school_id, db: Session, data: TermCreate):
    query = db.exec(select(Term).where(Term.school_id == school_id, Term.id == id)).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.")
    

    if(term_exist(school_id, data.name, db) and data.name != query.name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="It have been created, try a different year.")
    
    
    data = data.model_dump(exclude_unset=True) # we need only the data sent by the client, excluding any values that would be there just for being the default values
    query.sqlmodel_update(data)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query






