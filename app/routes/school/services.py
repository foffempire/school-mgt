from datetime import date, datetime
from fastapi import HTTPException, status
from sqlmodel import Session, select
from app.db.models import School
from app.security.security import get_password_hash
from .schema import SchoolCreate, SchoolUpdate


def create_school(session: Session, school: SchoolCreate):
    
    query = School.model_validate(school)
    session.add(query)
    session.commit()
    session.refresh(query)
    return query




def get_school(id: str, session: Session):
    query = select(School).where(School.id == id).where(School.is_active == True)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="School not found")
    return result
    



def update_school(id: str, school: SchoolUpdate, session: Session):
    try:
        query = session.exec(select(School).where(School.id == id)).first()       
        data = school.model_dump(exclude_unset=True) # we need only the data sent by the client, excluding any values that would be there just for being the default values
        query.sqlmodel_update(data)
        session.add(query)
        session.commit()
        session.refresh(query)
        return query
    except:
        session.rollback()
        raise HTTPException(status_code=404, detail="School not found")


def delete_school(id: str, session: Session):
    try:
        query = session.exec(select(School).where(School.id == id)).one()
        query.is_deleted = True
        query.is_active = False
        query.date_deleted = datetime.now()
        session.add(query)
        session.commit()
        return {"success": "Deleted successfully"}
    except:
        session.rollback()
        raise HTTPException(status_code=404, detail="School not found")