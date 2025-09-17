from sqlmodel import Session, select
from app.db.models import Teacher, Student, Class
from .schema import ClassCreate


# --- Class ---
def get_classes(session: Session):
    return session.exec(select(Class)).all()

def create_class(session: Session, school_class: ClassCreate):
    query = Class.model_validate(school_class)
    session.add(query)
    session.commit()
    session.refresh(query)
    return query
