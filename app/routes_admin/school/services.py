from datetime import date, datetime
from fastapi import HTTPException, status
from sqlmodel import Session, select
from app.db.models import School
from .schema import SchoolCreate, SchoolUpdate


def get_schools(session: Session):
    return session.exec(select(School)).all()


def get_school(school_uid: str, session: Session):
    try:
        query = select(School).where(School.school_uid == school_uid).where(School.is_active == True)
        result = session.exec(query).one()
        return result
    except:
        session.rollback()
        raise HTTPException(status_code=404, detail="School not found")


def create_school(session: Session, school: SchoolCreate):
    try:
        query = School.model_validate(school)
        session.add(query)
        session.commit()
        session.refresh(query)
        return query
    except:
        session.rollback()
        raise HTTPException(status_code=404, detail="School not created")


def update_school(school_uid: str, school: SchoolUpdate, session: Session):
    try:
        query = session.exec(select(School).where(School.school_uid == school_uid)).one()       
        data = school.model_dump(exclude_unset=True) # we need only the data sent by the client, excluding any values that would be there just for being the default values
        query.sqlmodel_update(data)
        session.add(query)
        session.commit()
        session.refresh(query)
        return query
    except:
        session.rollback()
        raise HTTPException(status_code=404, detail="School not found")


def delete_school(school_uid: str, session: Session):
    try:
        query = session.exec(select(School).where(School.school_uid == school_uid)).one()
        query.is_deleted = True
        query.is_active = False
        query.date_deleted = datetime.now()
        session.add(query)
        session.commit()
        return {"success": "Deleted successfully"}
    except:
        session.rollback()
        raise HTTPException(status_code=404, detail="School not found")