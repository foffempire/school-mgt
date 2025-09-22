from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4
from datetime import datetime, date, time, timezone
from enum import Enum


# student can login with email/student number
# teacher can login with email/teacher number
# staff can login with email/staff number
# super can only login with email

class Role(str, Enum):
    SUPER = "super"
    ADMIN = "admin"
    STAFF = "staff"
    TEACHER = "teacher"
    STUDENT = "student"
    PARENT = "parent"


# ============= WORK FLOW ====================
# user creates a school, and uses the school id to create an account
# create a different login table for teachers, students and parents to login


class School(SQLModel, table=True):
    id: str = Field(primary_key=True, unique=True, default_factory=lambda: str(uuid4()), index=True, nullable=False)
    name: str
    address: Optional[str] = None
    country: Optional[str] = None
    logo: Optional[str] = None  
    referrer: Optional[str] = None 
    is_active: bool = Field(default=True)
    is_premium: bool = Field(default=False)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_deleted: bool = Field(default=False)
    date_deleted: Optional[date] = None
    date_created: date = Field(default_factory=datetime.now)

    adminaccount: List["AdminAccount"] = Relationship(back_populates="school")
    staff: List["Staff"] = Relationship(back_populates="school")
    teacher: List["Teacher"] = Relationship(back_populates="school")
    parent: List["Parent"] = Relationship(back_populates="school")
    arm: List["Arm"] = Relationship(back_populates="school")
    class_: List["Class_"] = Relationship(back_populates="school")
    subject: List["Subject"] = Relationship(back_populates="school")
    student: List["Student"] = Relationship(back_populates="school")
    announcement: List["Announcement"] = Relationship(back_populates="school")
    events: List["Events"] = Relationship(back_populates="school")
    # Relationships
    enrollment: Optional["Enrollments"] = Relationship(back_populates="school")


class AdminAccount (SQLModel, table=True):
    id: str = Field(primary_key=True, unique=True, default_factory=lambda: str(uuid4()), index=True, nullable=False)
    school_id: str = Field(foreign_key="school.id")
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: str = Field(unique=True, index=True)
    password: str
    role: Role = 'admin' 
    is_active: bool = Field(default=True)
    date_created: date = Field(default_factory=datetime.now)

    school: Optional[School] = Relationship(back_populates="adminaccount")
    


class UserCreate(SQLModel):
    school_id: str = Field(foreign_key="school.id")
    firstname: str
    lastname: str
    othername: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    marital_status: str = None
    address: Optional[str] = None
    blood_group: Optional[str] = None
    Religion: Optional[str] = None
    bio: Optional[str] = None
    date_of_birth: Optional[date] = None
    image: Optional[str] = None


class UserBase(UserCreate):    
    id: str = Field(primary_key=True, unique=True, default_factory=lambda: str(uuid4()), index=True, nullable=False)
    is_active: bool = Field(default=True)
    is_deleted: bool = Field(default=False)
    date_created: date = Field(default_factory=datetime.now)
    date_updated: Optional[date] =  Field(default=None, sa_column_kwargs={"onupdate": datetime.now})
    date_deleted: Optional[date] = None


class Staff(UserBase, table=True):
    staff_no: Optional[str] = Field(default=None, unique=True)
    position: Optional[str] = None
    role: Role = 'staff'
    hire_date: date
    qualification: Optional[str] = None
    nok_names: Optional[str] = None
    nok_address: Optional[str] = None
    nok_phone: Optional[str] = None
    nok_email: Optional[str] = None
    nok_relationship: Optional[str] = None

    # Relationships will be defined in specific user types
    school: Optional[School] = Relationship(back_populates="staff")


class Teacher(UserBase, table=True):
    teacher_no: Optional[str] = Field(default=None, unique=True)
    role: Role = 'teacher'
    hire_date: date = None
    qualification: Optional[str] = None
    nok_names: Optional[str] = None
    nok_address: Optional[str] = None
    nok_phone: Optional[str] = None
    nok_email: Optional[str] = None
    nok_relationship: Optional[str] = None
    class_managed: Optional[str] = None
    arm: Optional[str] = None
    
    # Relationships
    school: Optional[School] = Relationship(back_populates="teacher")
    teacher_subjects: List["TeacherSubject"] = Relationship(back_populates="teacher")
    schedules: List["Schedule"] = Relationship(back_populates="teacher")


class Parent(UserBase, table=True):
    role: Role = 'parent'
    occupation: Optional[str] = None
    
    # Relationship
    school: Optional[School] = Relationship(back_populates="parent")
    students: List["Student"] = Relationship(back_populates="parent")


class Arm(SQLModel, table=True):
    id: str = Field(primary_key=True, unique=True, default_factory=lambda: str(uuid4()), index=True, nullable=False)
    school_id: str = Field(foreign_key="school.id")
    name: str
    is_active: bool = Field(default=True)

    school: Optional[School] = Relationship(back_populates="arm")
    students: Optional["Student"] = Relationship(back_populates="arm")
    enrollment: Optional["Enrollments"] = Relationship(back_populates="arm")
    schedules: Optional["Schedule"] = Relationship(back_populates="arm")


class Class_(SQLModel, table=True):
    id: str = Field(primary_key=True, unique=True, default_factory=lambda: str(uuid4()), index=True, nullable=False)
    school_id: str = Field(foreign_key="school.id")
    name: str
    room_number: Optional[str] = None
    academic_year: Optional[str] = None
    is_active: bool = Field(default=True)
    
    # Relationships
    school: Optional[School] = Relationship(back_populates="class_")
    students: List["Student"] = Relationship(back_populates="class_")
    schedules: List["Schedule"] = Relationship(back_populates="class_")
    enrollment: Optional["Enrollments"] = Relationship(back_populates="class_")


class Subject(SQLModel, table=True):
    id: str = Field(primary_key=True, unique=True, default_factory=lambda: str(uuid4()), index=True, nullable=False)
    school_id: str = Field(foreign_key="school.id")
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None
    type: Optional[str] = Field(default="Core")
    code: Optional[str] = Field(unique=True)
    is_active: bool = Field(default=True)
    
    # Relationships
    school: Optional[School] = Relationship(back_populates="subject")
    teacher_subjects: List["TeacherSubject"] = Relationship(back_populates="subject")
    schedules: List["Schedule"] = Relationship(back_populates="subject")


# Association table for many-to-many between Teacher and Subject
class TeacherSubject(SQLModel, table=True):
    teacher_id: Optional[str] = Field(default=None, foreign_key="teacher.id", primary_key=True)
    subject_id: Optional[str] = Field(default=None, foreign_key="subject.id", primary_key=True)
    
    teacher: "Teacher" = Relationship(back_populates="teacher_subjects")
    subject: "Subject" = Relationship(back_populates="teacher_subjects")



class Student(UserBase, table=True):
    role: Role = 'student'
    student_no: Optional[str] = Field(default=None, unique=True)
    enrollment_date: date = None
    class_id: Optional[str] = Field(default=None, foreign_key="class_.id")
    arm_id: Optional[str] = Field(default=None, foreign_key="arm.id")
    parent_id: Optional[str] = Field(default=None, foreign_key="parent.id")
    
    # Relationships
    school: Optional[School] = Relationship(back_populates="student")
    class_: Optional["Class_"] = Relationship(back_populates="students")
    arm: Optional["Arm"] = Relationship(back_populates="students")
    parent: Optional["Parent"] = Relationship(back_populates="students")
    enrollment: Optional["Enrollments"] = Relationship(back_populates="students")



class Schedule(SQLModel, table=True):
    id: str = Field(primary_key=True, unique=True, default_factory=lambda: str(uuid4()), index=True, nullable=False)
    school_id: str = Field(foreign_key="school.id")
    day_of_week: str # e.g. 'Monday'
    start_time: time
    end_time: time
    is_active: bool = Field(default=True)
    teacher_id: Optional[str] = Field(foreign_key="teacher.id")
    class_id: Optional[str] = Field(foreign_key="class_.id")
    arm_id: Optional[str] = Field(foreign_key="arm.id")
    subject_id: Optional[str] = Field(foreign_key="subject.id")
    
    # Relationships
    teacher: "Teacher" = Relationship(back_populates="schedules")
    class_: "Class_" = Relationship(back_populates="schedules")
    arm: "Arm" = Relationship(back_populates="schedules")
    subject: "Subject" = Relationship(back_populates="schedules")



class Announcement(SQLModel, table=True):
    id: str = Field(primary_key=True, unique=True, default_factory=lambda: str(uuid4()), index=True, nullable=False)
    school_id: str = Field(foreign_key="school.id")
    title: str
    content: str
    date_posted: datetime = Field(default_factory=datetime.now(timezone.utc))
    is_active: bool = Field(default=True)
    created_by: Optional[str]
    target_audience: Optional[str] = None  # Could be "all", "teachers", "students", etc.
    date_created: date = Field(default_factory=datetime.now)
    
    # Relationship
    school: Optional[School] = Relationship(back_populates="announcement")


class Events(SQLModel, table=True):
    id: str = Field(primary_key=True, unique=True, default_factory=lambda: str(uuid4()), index=True, nullable=False)
    school_id: str = Field(foreign_key="school.id")
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    location: Optional[str] = None
    is_active: bool = Field(default=True)
    created_by: Optional[str]
    event_type: Optional[str] = None  # e.g., "meeting", "holiday", "exam", etc.
    date_created: date = Field(default_factory=datetime.now)
    
    # Relationship
    school: Optional[School] = Relationship(back_populates="events")



class Grades(SQLModel, table=True):
    id: str = Field(primary_key=True, unique=True, default_factory=lambda: str(uuid4()), index=True, nullable=False)
    school_id: str = Field(foreign_key="school.id")
    title: str #eg A+
    point: Optional[str] = None #eg 4.50
    percent_min: Optional[int]  #eg 85%
    percent_max: Optional[int] #eg 100%
    comment: Optional[str] #eg Distinction
    is_active: bool = Field(default=True)


class AcademicSession(SQLModel, table=True):
    id: str = Field(primary_key=True, unique=True, default_factory=lambda: str(uuid4()), index=True, nullable=False)
    school_id: str = Field(foreign_key="school.id")
    name: str #eg 2025/2026
    current: bool =Field(default=False)
    is_active: bool = Field(default=True)


    # Relationships
    enrollment: Optional["Enrollments"] = Relationship(back_populates="academicsession")



class Term (SQLModel, table=True):
    id: str = Field(primary_key=True, unique=True, default_factory=lambda: str(uuid4()), index=True, nullable=False)
    school_id: str = Field(foreign_key="school.id")
    name: str # e.g. 'First Term'
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    


class Enrollments(SQLModel, table=True):
    id: str = Field(primary_key=True, unique=True, default_factory=lambda: str(uuid4()), index=True, nullable=False)
    school_id: str = Field(foreign_key="school.id")
    student_id: str = Field(foreign_key="student.id")
    class_id: str = Field(foreign_key="class_.id")
    arm_id: str = Field(foreign_key="arm.id")
    academicsession_id: str = Field(foreign_key="academicsession.id")
    enrollment_date: date = Field(default_factory=datetime.now)
    status: str = Field(default='enrolled', nullable=True) #eg enrolled, graduated, expelled, withdrawn, other 

    # Relationships
    school: Optional[School] = Relationship(back_populates="enrollment")
    students: List["Student"] = Relationship(back_populates="enrollment")
    class_: List["Class_"] = Relationship(back_populates="enrollment") 
    arm: List["Arm"] = Relationship(back_populates="enrollment") 
    academicsession: List["AcademicSession"] = Relationship(back_populates="enrollment") 
    


class Attendance (SQLModel, table=True):
    id: str = Field(primary_key=True, unique=True, default_factory=lambda: str(uuid4()), index=True, nullable=False)
    school_id: str = Field(foreign_key="school.id")
    student_id: str = Field(foreign_key="student.id")
    class_id: str = Field(foreign_key="class_.id")
    arm_id: str = Field(foreign_key="arm.id")
    status: Optional[str] = None
    reason: Optional[str] = None
    recorded_by: str
    date_created: date = Field(default_factory=datetime.now)