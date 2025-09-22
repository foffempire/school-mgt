from typing import List
from fastapi import HTTPException, status
from sqlmodel import Session, select
from app.db.models import Arm
from app.security.security import is_owner
from .schema import ArmCreate



def arm_exist(school_id, arm_name,db: Session):
    stmt = db.exec(select(Arm).where(Arm.name == arm_name, Arm.school_id == school_id, Arm.is_active == True)).first()
    if stmt:
        return True
    else:
        return False
    


def get_arms(school_id, db: Session):
    return db.exec(select(Arm).where(Arm.school_id == school_id, Arm.is_active == True).order_by(Arm.name)).all()


def create_arm(school_id, db: Session, school_arm: List[ArmCreate]):

    for p in school_arm:         
        if arm_exist(school_id, p.name, db):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{p.name} already created")


        data = {
            "school_id": school_id,
            "name": p.name,
        }
        query = Arm.model_validate(data)
        db.add(query)
        db.commit()
        db.refresh(query)
    
    return {"data":"successful"}



def get_arm(id: str, school_id: str, db: Session):
    query = db.exec(select(Arm).where(Arm.id == id, Arm.school_id == school_id, Arm.is_active == True)).first()
    if not query:
        raise HTTPException(status_code=404, detail="Arm not found")
    
    return query
    

def update_arm(id: str, school_id: str, school_arm: ArmCreate, db: Session):        

    query = db.exec(select(Arm).where(Arm.id == id, Arm.school_id == school_id)).first()
    if not query:
        raise HTTPException(status_code=404, detail="Arm not found")
    
            
    data = school_arm.model_dump(exclude_unset=True) # we need only the data sent by the client, excluding any values that would be there just for being the default values
    query.sqlmodel_update(data)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def deactivate_arm(id: str, school_id, db: Session):
    query = db.exec(select(Arm).where(Arm.id == id, Arm.school_id == school_id)).first()
    if not query:
            raise HTTPException(status_code=404, detail="Arm not found")
    query.is_active = False
    db.add(query)
    db.commit()
    return {"success": "Deleted successfully"}
    