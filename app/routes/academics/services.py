from datetime import datetime
from fastapi import HTTPException, status
from sqlmodel import Session, select
from app.db.models import AcademicSession, Student
from .schema import SessionCreate


def session_exist(school_id, name, db: Session):
    stmt = db.exec(select(AcademicSession).where(AcademicSession.name == name, AcademicSession.school_id == school_id)).first()
    if stmt:
        return True
    else:
        return False



def create_academic_session(school_id, db: Session, data: SessionCreate):

    if(session_exist(school_id, data.name, db )):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You already created this academic year.")
    

    sid = {"school_id": school_id}
    query = AcademicSession.model_validate(data.model_dump() | sid)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def get_academic_sessions(school_id, db: Session):
    return db.exec(select(AcademicSession).where(AcademicSession.school_id == school_id, AcademicSession.is_active == True)).all()



def get_academic_session(year_id, school_id, db: Session):
    query = db.exec(select(AcademicSession).where(AcademicSession.school_id == school_id, AcademicSession.id == year_id, AcademicSession.is_active == True)).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    return query



def edit_academic_session(id, school_id, db: Session, data: SessionCreate):
    query = db.exec(select(AcademicSession).where(AcademicSession.school_id == school_id, AcademicSession.id == id, AcademicSession.is_active == True)).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.")
    

    if(session_exist(school_id, data.name, db) and data.name != query.name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="It have been created, try a different year.")
    
    
    data = data.model_dump(exclude_unset=True) # we need only the data sent by the client, excluding any values that would be there just for being the default values
    query.sqlmodel_update(data)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def deactivate_academic_session(id, school_id, db: Session):
    query = db.exec(select(AcademicSession).where(AcademicSession.school_id == school_id, AcademicSession.id == id, AcademicSession.is_active == True)).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found.")
    
    
    query.is_active = False
    db.add(query)
    db.commit()
    return {"success": "Deleted Successfully"} 


