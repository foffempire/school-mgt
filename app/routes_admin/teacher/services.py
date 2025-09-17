from sqlmodel import Session, select
from app.db.models import Teacher
from .schema import TeacherCreate


# --- Class ---
def get_teachers(session: Session):
    return session.exec(select(Teacher)).all()

def create_teacher(session: Session, teacher: TeacherCreate):
    query = Teacher.model_validate(teacher)
    session.add(query)
    session.commit()
    session.refresh(query)
    return query