from .UUIDColumn import UUIDColumn, UUIDFKey
from sqlalchemy import Column, DateTime, String, ForeignKey, Boolean
from .BaseModel import BaseModel
import sqlalchemy

from .BaseModel import BaseModel

class StudentExamLink(BaseModel):
    """
    Represents a link between exams and students.
    """
    __tablename__ = "StudentExamLinks"

    id = UUIDColumn()

    exam_id = Column(ForeignKey("exams.id"), index=True, nullable=True, comment="Foreign key referencing the exam")
    student_id = Column(ForeignKey("students.id"), index=True, nullable=True, comment="Foreign key referencing the student")

    valid = Column(Boolean, default=True, comment="Indicates if the exam type is valid")