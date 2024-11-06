from .UUIDColumn import UUIDColumn, UUIDFKey
from sqlalchemy import Column, DateTime, Boolean, ForeignKey, Float
from .BaseModel import BaseModel
from sqlalchemy.orm import relationship
import sqlalchemy

class ExamResultModel(BaseModel):
    """
    Represents an exam entry associated with an exam type and a student admission.
    """
    __tablename__ = "exam_results"

    id = UUIDColumn()

    score = Column(Float, nullable=False, default=0)

    exam_id = Column(ForeignKey("exams.id"), index=True, comment="Foreign key referencing the associated exam")
    exam = relationship("ExamModel", back_populates="exam_results")

    student_admission_id = Column(ForeignKey("studentadmissions.id"), index=True, comment="Foreign key referencing the related student admission")
    student_admission = relationship("StudentAdmissionModel", back_populates="student_admissions")

    valid = Column(Boolean, default=True, comment="Indicates if the exam entry is valid")
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when the exam was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last modification")
    createdby = UUIDFKey(nullable=True, comment="User ID of the creator")
    changedby = UUIDFKey(nullable=True, comment="User ID of the last modifier")
    rbacobject = UUIDFKey(nullable=True, comment="User or group ID that controls access to the exam entry")
