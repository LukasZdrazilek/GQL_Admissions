from sqlalchemy import Column, ForeignKey, Float
from .BaseModel import BaseModel
from sqlalchemy.orm import relationship

class ExamResultModel(BaseModel):
    """
    Represents an exam entry associated with an exam type and a student admission.
    """
    __tablename__ = "exam_results"

    score = Column(Float, nullable=False, default=0)

    exam_id = Column(ForeignKey("exams.id"), index=True, comment="Foreign key referencing the associated exam")
    exam = relationship("ExamModel", back_populates="exam_results")

    student_admission_id = Column(ForeignKey("student_admissions.id"), index=True, comment="Foreign key referencing the related student admission")
    student_admission = relationship("StudentAdmissionModel", back_populates="student_admissions")