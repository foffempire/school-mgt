from sqlmodel import Session, select
from app.db.models import Student
from .schema import StudentCreate

# --- Student ---
def get_students(session: Session):
    return session.exec(select(Student)).all()

def create_student(session: Session, student: StudentCreate):
    query = Student.model_validate(student)
    session.add(query)
    session.commit()
    session.refresh(query)
    return query
