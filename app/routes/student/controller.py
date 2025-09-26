from fastapi import APIRouter, File, UploadFile
from typing import List
from app.db.database import SessionDep
from app.image.services import upload_image
from app.security.oauth2 import CurrentUserDep
from .schema import StudentCreate, StudentId, StudentPublic, StudentUpdate
from .services import archive_student, deactivate_student, edit_student, edit_student_image, get_archived_students, get_student, get_students, create_student, unarchive_student

router = APIRouter(prefix="/v1", tags=["Students"])

@router.get("/students", response_model=List[StudentPublic])
def read_students(current_user: CurrentUserDep, db: SessionDep):
    return get_students(current_user.school_id, db)



@router.get("/students/{student_id}", response_model=StudentPublic)
def read_student(student_id, current_user: CurrentUserDep, db: SessionDep):
    return get_student(student_id, current_user.school_id, db)



@router.post("/students", response_model=StudentPublic)
def add_student(current_user: CurrentUserDep, student: StudentCreate, db: SessionDep):
    return create_student(current_user.school_id, db, student)



@router.patch("/students/{student_id}", response_model=StudentPublic)
def update_student(student_id, current_user: CurrentUserDep, student: StudentUpdate, db: SessionDep):
    return edit_student(student_id, current_user.school_id, db, student)



@router.patch("/students/{student_id}/image", response_model=StudentPublic)
async def update_student_image(student_id, current_user: CurrentUserDep, db: SessionDep, file: UploadFile  = File(...)):
    return await edit_student_image(file, student_id, current_user.school_id, db)
    # return await upload_image(file)



@router.get("/student-archives", response_model=List[StudentPublic])
def archived_students(current_user: CurrentUserDep, db: SessionDep):
    return get_archived_students(current_user.school_id, db)


@router.patch("/student-archives")
def archive_students(student_ids: List[StudentId], current_user: CurrentUserDep, db: SessionDep):
    return archive_student(student_ids, current_user.school_id, db)


@router.patch("/student-unarchives")
def unarchive_students(student_ids: List[StudentId], current_user: CurrentUserDep, db: SessionDep):
    return unarchive_student(student_ids, current_user.school_id, db)


@router.patch("/student-delete")
def delete_students(student_ids: List[StudentId], current_user: CurrentUserDep, db: SessionDep):
    return deactivate_student(student_ids, current_user.school_id, db)