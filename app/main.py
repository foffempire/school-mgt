from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import Settings
from app.db.models import Schedule, UserBase
from .db.database import SessionDep, create_db_and_tables
from sqlmodel import select

from .routes.auth import controller as authController
from .routes.admin import controller as adminController
from .routes.class_ import controller as classController
from .routes.class_arm import controller as armController
from .routes.school import controller as schoolController
from .routes.teacher import controller as teacherController
from .routes.student import controller as studentController
from .routes.parent import controller as parentController
from .routes.staff import controller as staffController

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     create_db_and_tables()
#     yield

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root(user: Schedule):
    data = {"name":"john"}
    return data


app.include_router(authController.router)
app.include_router(schoolController.router)
app.include_router(adminController.router)
app.include_router(classController.router)
app.include_router(armController.router)
app.include_router(teacherController.router)
app.include_router(studentController.router)
app.include_router(parentController.router)
app.include_router(staffController.router)

# @app.post("/add")
# async def addUser(user: UserBase, session: SessionDep) -> User:
#     query = User.model_validate(user)
#     session.add(query)
#     session.commit()
#     session.refresh(query)
#     return query

# @app.get("/get")
# async def getUser(session: SessionDep) -> list[User]:
#     query = select(User)
#     results = session.exec(query)
#     return results.all()


# @app.get("/get/{id}")
# async def getUserId(id:str, session: SessionDep) -> User:
#     query = select(User).where(User.id == id)
#     result = session.exec(query)
#     return result.one()