from fastapi import HTTPException
from sqlmodel import Session, select
from app.db.models import Class_
from app.security.security import is_owner
from .schema import ClassCreate


# --- Class ---
def get_classes(school_id, db: Session):
    return db.exec(select(Class_).where(Class_.school_id == school_id, Class_.is_active == True).order_by(Class_.name)).all()


def create_class(school_id, db: Session, school_class: ClassCreate):
    data = {
        "school_id": school_id,
        "name": school_class.name,
        "room_number": school_class.room_number,
        "academic_year": school_class.academic_year
    }
    query = Class_.model_validate(data)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def get_class(id: str, school_id: str, db: Session):
    query = db.exec(select(Class_).where(Class_.id == id, Class_.school_id == school_id, Class_.is_active == True)).first()
    if not query:
        raise HTTPException(status_code=404, detail="Class not found")
    
    return query
    

def update_class(id: str, school_id: str, class_: ClassCreate, db: Session):        

    query = db.exec(select(Class_).where(Class_.id == id, Class_.school_id == school_id)).first()
    if not query:
        raise HTTPException(status_code=404, detail="Class not found")
    
            
    data = class_.model_dump(exclude_unset=True) # we need only the data sent by the client, excluding any values that would be there just for being the default values
    query.sqlmodel_update(data)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def deactivate_class(id: str, school_id, db: Session):
    query = db.exec(select(Class_).where(Class_.id == id, Class_.school_id == school_id)).first()
    if not query:
            raise HTTPException(status_code=404, detail="Class not found")
    query.is_active = False
    db.add(query)
    db.commit()
    return {"success": "Deleted successfully"}
    