from datetime import date, datetime
from fastapi import HTTPException, status
from sqlmodel import Session, select
from app.db.models import School, Student
from app.security.security import get_password_hash
from .schema import SchoolCreate, SchoolUpdate


def create_school(db: Session, school: SchoolCreate):
    
    query = School.model_validate(school)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query




def get_school(id: str, db: Session):
    query = select(School).where(School.id == id).where(School.is_active == True)
    result = db.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="School not found")
    return result
    



def update_school(id: str, school: SchoolUpdate, db: Session):
    try:
        query = db.exec(select(School).where(School.id == id)).first()       
        data = school.model_dump(exclude_unset=True) # we need only the data sent by the client, excluding any values that would be there just for being the default values
        query.sqlmodel_update(data)
        db.add(query)
        db.commit()
        db.refresh(query)
        return query
    except:
        db.rollback()
        raise HTTPException(status_code=404, detail="School not found")


def delete_school(id: str, db: Session):
    try:
        query = db.exec(select(School).where(School.id == id)).one()
        query.is_deleted = True
        query.is_active = False
        query.date_deleted = datetime.now()
        db.add(query)
        db.commit()
        return {"success": "Deleted successfully"}
    except:
        db.rollback()
        raise HTTPException(status_code=404, detail="School not found")
    
