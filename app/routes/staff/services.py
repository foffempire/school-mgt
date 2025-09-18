from datetime import datetime
from fastapi import HTTPException, status
from sqlmodel import Session, select
from app.db.models import Staff
from .schema import StaffCreate, StaffUpdate



def staff_number_exist(school_id, staff_number, db: Session):
    stmt = db.exec(select(Staff).where(Staff.staff_no == staff_number, Staff.school_id == school_id)).first()
    if stmt:
        return True
    else:
        return False


def staff_email_exist(school_id, email, db: Session):
    stmt = db.exec(select(Staff).where(Staff.email == email, Staff.school_id == school_id)).first()
    if stmt:
        return True
    else:
        return False



def get_staffs(school_id, db: Session):
    return db.exec(select(Staff).where(Staff.school_id == school_id, Staff.is_active == True)).all()


def get_staff(staff_id, school_id, db: Session):
    query = db.exec(select(Staff).where(Staff.school_id == school_id, Staff.id == staff_id, Staff.is_active == True)).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    
    return query


def create_staff(school_id, db: Session, staff_data: StaffCreate):

    if(staff_email_exist(school_id, staff_data.email, db )):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email have been used.")
    
    if(staff_number_exist(school_id, staff_data.staff_no, db )):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Staff number have been used.")

    sid = {"school_id": school_id}
    query = Staff.model_validate(staff_data.model_dump() | sid)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def edit_staff(staff_id, school_id, db: Session, staff_data: StaffUpdate):
    query = db.exec(select(Staff).where(Staff.school_id == school_id, Staff.id == staff_id, Staff.is_active == True)).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found.")
    

    if(staff_email_exist(school_id, staff_data.email, db) and staff_data.email != query.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email have been used.")
    
    if(staff_number_exist(school_id, staff_data.staff_no, db) and staff_data.staff_no != query.staff_no):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Staff number have been used.")
    
    data = staff_data.model_dump(exclude_unset=True) # we need only the data sent by the client, excluding any values that would be there just for being the default values
    query.sqlmodel_update(data)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def deactivate_staff(staff_id, school_id, db: Session):
    query = db.exec(select(Staff).where(Staff.school_id == school_id, Staff.id == staff_id, Staff.is_active == True)).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found.")
    
    
    query.is_active = False
    query.is_deleted = True
    query.date_deleted = datetime.now()
    db.add(query)
    db.commit()
    return {"success": "Deleted Successfully"} 


