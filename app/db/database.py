from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

import app.db.models

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:science@localhost/schoolmgtapp"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]