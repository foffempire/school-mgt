from sqlmodel import Session, select
from app.db.models import Parent
from .schema import ParentCreate


# --- Class ---
def get_parents(session: Session):
    return session.exec(select(Parent)).all()

def create_parent(session: Session, parent: ParentCreate):
    query = Parent.model_validate(parent)
    session.add(query)
    session.commit()
    session.refresh(query)
    return query
