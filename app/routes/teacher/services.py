from datetime import datetime
from fastapi import HTTPException, status
from sqlmodel import Session, select
from app.db.models import Teacher
from .schema import TeacherCreate, TeacherUpdate



def teacher_number_exist(school_id, teacher_number,db: Session):
    stmt = db.exec(select(Teacher).where(Teacher.teacher_no == teacher_number, Teacher.school_id == school_id)).first()
    if stmt:
        return True
    else:
        return False


def teacher_email_exist(school_id, email, db: Session):
    stmt = db.exec(select(Teacher).where(Teacher.email == email, Teacher.school_id == school_id)).first()
    if stmt:
        return True
    else:
        return False



def get_teachers(school_id, db: Session):
    return db.exec(select(Teacher).where(Teacher.school_id == school_id, Teacher.is_active == True)).all()


def get_teacher(teacher_id, school_id, db: Session):
    query = db.exec(select(Teacher).where(Teacher.school_id == school_id, Teacher.id == teacher_id, Teacher.is_active == True)).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    
    return query


def create_teacher(school_id, db: Session, teacher_data: TeacherCreate):

    if(teacher_email_exist(school_id, teacher_data.email, db )):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email have been used.")
    
    if(teacher_number_exist(school_id, teacher_data.teacher_no, db )):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Teacher number have been used.")

    sid = {"school_id": school_id}
    query = Teacher.model_validate(teacher_data.model_dump() | sid)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def edit_teacher(teacher_id, school_id, db: Session, teacher_data: TeacherUpdate):
    query = db.exec(select(Teacher).where(Teacher.school_id == school_id, Teacher.id == teacher_id, Teacher.is_active == True)).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found.")
    

    if(teacher_email_exist(school_id, teacher_data.email, db) and teacher_data.email != query.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email have been used.")
    
    if(teacher_number_exist(school_id, teacher_data.teacher_no, db) and teacher_data.teacher_no != query.teacher_no):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Teacher number have been used.")
    
    data = teacher_data.model_dump(exclude_unset=True) # we need only the data sent by the client, excluding any values that would be there just for being the default values
    query.sqlmodel_update(data)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def deactivate_teacher(teacher_id, school_id, db: Session):
    query = db.exec(select(Teacher).where(Teacher.school_id == school_id, Teacher.id == teacher_id, Teacher.is_active == True)).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found.")
    
    
    query.is_active = False
    query.is_deleted = True
    query.date_deleted = datetime.now()
    db.add(query)
    db.commit()
    return {"success": "Deleted Successfully"} 



# def assign_teacher_class(teacher_id, school_id, db: Session, class_name):
#     query = db.exec(select(Teacher).where(Teacher.school_id == school_id, Teacher.id == teacher_id, Teacher.is_active == True)).first()
#     if not query:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found.")
    
    
#     query.class_managed = class_name
#     db.add(query)
#     db.commit()
#     return query
