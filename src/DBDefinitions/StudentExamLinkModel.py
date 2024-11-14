from sqlalchemy import Column, ForeignKey
from .BaseModel import BaseModel

class StudentExamLinkModel(BaseModel):
    """
    Represents a link between exams and students.
    """
    __tablename__ = "student_exam_links"

    exam_id = Column(ForeignKey("exams.id"), index=True, nullable=True, comment="Foreign key referencing the exam")
    student_id = Column(ForeignKey("student_admissions.id"), index=True, nullable=True, comment="Foreign key referencing the student")
