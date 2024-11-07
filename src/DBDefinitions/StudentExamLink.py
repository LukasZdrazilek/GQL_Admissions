from sqlalchemy import Column, ForeignKey
from .BaseModel import BaseModel

class StudentExamLink(BaseModel):
    """
    Represents a link between exams and students.
    """
    __tablename__ = "StudentExamLinks"

    exam_id = Column(ForeignKey("exams.id"), index=True, nullable=True, comment="Foreign key referencing the exam")
    student_id = Column(ForeignKey("students.id"), index=True, nullable=True, comment="Foreign key referencing the student")
