from .UUIDColumn import UUIDColumn, UUIDFKey
from sqlalchemy import Column, DateTime, String, ForeignKey, Boolean
from .BaseModel import BaseModel
import sqlalchemy


class StudentExamLink(BaseModel):
    """
    Represents a link between exams and students.
    """
    __tablename__ = "StudentExamLinks"

    id = UUIDColumn()

    exam_id = Column(ForeignKey("exams.id"), index=True, nullable=True, comment="Foreign key referencing the exam")
    student_id = Column(ForeignKey("students.id"), index=True, nullable=True, comment="Foreign key referencing the student")

    valid = Column(Boolean, default=True, comment="Indicates if the exam type is valid")
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when the exam type was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last modification")
    createdby = UUIDFKey(nullable=True, comment="User ID of the creator")
    changedby = UUIDFKey(nullable=True, comment="User ID of the last modifier")
    rbacobject = UUIDFKey(nullable=True, comment="User or group ID that controls access to the exam type")