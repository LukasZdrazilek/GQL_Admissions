from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from .BaseModel import BaseModel
import uuid

class ExamResultModel(BaseModel):
    """
    Represents an exam entry associated with an exam type and a student admission.
    """
    __tablename__ = "exam_results"

    score: Mapped[float] = mapped_column(nullable= True, default=None, comment="Score achieved in the exam")
    exam_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exams.id"), index=True, nullable= True, default=None, comment="Foreign key referencing the associated exam")
    student_admission_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("student_admissions.id"), index=True, nullable= True, default=None, comment="Foreign key referencing the related student admission")

    exam = relationship("ExamModel", viewonly=True, lazy="joined")
    student_admission = relationship("StudentAdmissionModel", viewonly=True, lazy="joined")
