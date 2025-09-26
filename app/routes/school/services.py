from datetime import date, datetime
from fastapi import HTTPException, status
from sqlmodel import Session, select
from app.db.models import AcademicSession, Arm, Class_, Parent, School, Staff, Student, Teacher, Term
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
    


def school_info(school_id, db: Session):
    school = db.exec(select(School).where(School.id == school_id, School.is_active == True)).first()

    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    
    students = db.exec(select(Student).where(Student.school_id == school_id, Student.is_active == True)).all()
    teachers = db.exec(select(Teacher).where(Teacher.school_id == school_id, Teacher.is_active == True)).all()
    staffs = db.exec(select(Staff).where(Staff.school_id == school_id, Staff.is_active == True)).all()
    parents = db.exec(select(Parent).where(Parent.school_id == school_id, Parent.is_active == True)).all()
    classes_ = db.exec(select(Class_).where(Class_.school_id == school_id, Class_.is_active == True)).all()
    arms = db.exec(select(Arm).where(Arm.school_id == school_id, Arm.is_active == True)).all()
    sessions = db.exec(select(AcademicSession).where(AcademicSession.school_id == school_id, AcademicSession.is_active == True)).all()
    terms = db.exec(select(Term).where(Term.school_id == school_id)).all()

    return {
        "school": school,
        "students": students,
        "teachers": teachers,
        "staffs": staffs,
        "parents": parents,
        "classes": classes_,
        "arms": arms,
        "sessions": sessions,
        "terms": terms,
    }