from datetime import datetime
from fastapi import HTTPException, status
from sqlmodel import Session, select
from app.db.models import Parent
from .schema import ParentCreate, ParentUpdate



def parent_email_exist(school_id, email, db: Session):
    stmt = db.exec(select(Parent).where(Parent.email == email, Parent.school_id == school_id)).first()
    if stmt:
        return True
    else:
        return False



def get_parents(school_id, db: Session):
    return db.exec(select(Parent).where(Parent.school_id == school_id, Parent.is_active == True)).all()


def get_parent(parent_id, school_id, db: Session):
    query = db.exec(select(Parent).where(Parent.school_id == school_id, Parent.id == parent_id, Parent.is_active == True)).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent not found")
    
    return query


def create_parent(school_id, db: Session, parent_data: ParentCreate):

    if(parent_email_exist(school_id, parent_data.email, db )):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email have been used.")

    sid = {"school_id": school_id}
    query = Parent.model_validate(parent_data.model_dump() | sid)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def edit_parent(parent_id, school_id, db: Session, parent_data: ParentUpdate):
    query = db.exec(select(Parent).where(Parent.school_id == school_id, Parent.id == parent_id, Parent.is_active == True)).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent not found.")
    

    if(parent_email_exist(school_id, parent_data.email, db) and parent_data.email != query.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email have been used.")
    
    data = parent_data.model_dump(exclude_unset=True) # we need only the data sent by the client, excluding any values that would be there just for being the default values
    query.sqlmodel_update(data)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def get_archived_parents(school_id, db: Session):
    return db.exec(select(Parent).where(Parent.school_id == school_id, Parent.is_active == False, Parent.is_deleted == False)).all()



def archive_parent(parent_id, school_id, db: Session):
    query = db.exec(select(Parent).where(Parent.school_id == school_id, Parent.id == parent_id, Parent.is_active == True)).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent not found.")
    
    
    query.is_active = False
    db.add(query)
    db.commit()
    return {"success": "Parent moved to archive"} 



def deactivate_parent(parent_id, school_id, db: Session):
    query = db.exec(select(Parent).where(Parent.school_id == school_id, Parent.id == parent_id, Parent.is_active == True)).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent not found.")
    
    
    query.is_active = False
    query.is_deleted = True
    query.date_deleted = datetime.now()
    db.add(query)
    db.commit()
    return {"success": "Deleted Successfully"} 

