from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from .BaseModel import BaseModel


class StudentExamLinkModel(BaseModel):
    """
    Represents a link between exams and student admissions.
    """
    __tablename__ = "student_exam_links"

    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id"), index=True, default=None, nullable=True, comment="Foreign key referencing the exam")

    student_admission_id: Mapped[int] = mapped_column(ForeignKey("student_admissions.id"), index=True, default=None, nullable=True, comment="Foreign key referencing the student")
