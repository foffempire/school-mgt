from datetime import datetime
from typing import List
from fastapi import HTTPException, status
from sqlmodel import Session, select
from app.db.models import Student
from app.image.services import upload_image
from .schema import StudentCreate, StudentId, StudentUpdate



def student_number_exist(school_id, student_number,db: Session):
    stmt = db.exec(select(Student).where(Student.student_no == student_number, Student.school_id == school_id)).first()
    if stmt:
        return True
    else:
        return False


def student_email_exist(school_id, email, db: Session):
    if not email:
        return False
    
    stmt = db.exec(select(Student).where(Student.email == email, Student.school_id == school_id)).first()
    if stmt:
        return True
    else:
        return False


def get_students(school_id, db: Session):
    return db.exec(select(Student).where(Student.school_id == school_id, Student.is_active == True)).all()


def get_student(student_id, school_id, db: Session):
    query = db.exec(select(Student).where(Student.school_id == school_id, Student.id == student_id, Student.is_active == True)).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    return query


def create_student(school_id, db: Session, student_data: StudentCreate):

    if(student_email_exist(school_id, student_data.email, db )):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email have been used.")
    
    if(student_number_exist(school_id, student_data.student_no, db )):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Student number have been used.")

    sid = {"school_id": school_id}
    query = Student.model_validate(student_data.model_dump() | sid)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def edit_student(student_id, school_id, db: Session, student_data: StudentUpdate):
    query = db.exec(select(Student).where(Student.school_id == school_id, Student.id == student_id, Student.is_active == True)).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found.")
    

    if(student_email_exist(school_id, student_data.email, db) and student_data.email != query.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email have been used.")
    
    if(student_number_exist(school_id, student_data.student_no, db) and student_data.student_no != query.student_no):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Student number have been used.")
    
    data = student_data.model_dump(exclude_unset=True) # we need only the data sent by the client, excluding any values that would be there just for being the default values
    query.sqlmodel_update(data)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


async def edit_student_image(file, student_id, school_id, db: Session):
    query = db.exec(select(Student).where(Student.school_id == school_id, Student.id == student_id, Student.is_active == True)).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found.")
    
    filename = await upload_image(file)
    query.image = filename
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def archive_student(student_ids: List[StudentId], school_id, db: Session):
    for student_id in student_ids:
        query = db.exec(select(Student).where(Student.school_id == school_id, Student.id == student_id.id, Student.is_active == True)).first()
        if not query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One of the selected students not found.")
        
        
        query.is_active = False
        db.add(query)
        db.commit()
    return {"success": "Student(s) moved to archive"} 


def unarchive_student(student_ids: List[StudentId], school_id, db: Session):
    for student_id in student_ids:
        query = db.exec(select(Student).where(Student.school_id == school_id, Student.id == student_id.id, Student.is_active == False)).first()
        if not query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One of the selected students not  found.")
        
        
        query.is_active = True
        db.add(query)
        db.commit()

    return {"success": "Student(s) removed to archive"} 



def get_archived_students(school_id, db: Session):
    # archived students have is_active == false and is_deleted == false
    return db.exec(select(Student).where(Student.school_id == school_id, Student.is_active == False, Student.is_deleted == False)).all()


def deactivate_student(student_ids: List[StudentId], school_id, db: Session):
    for student_id in student_ids:
        query = db.exec(select(Student).where(Student.school_id == school_id, Student.id == student_id.id, Student.is_active == False)).first()
        if not query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found.")
        
        
        # query.is_active = False
        query.is_deleted = True
        query.date_deleted = datetime.now()
        db.add(query)
        db.commit()
    return {"success": "Deleted Successfully"} 


