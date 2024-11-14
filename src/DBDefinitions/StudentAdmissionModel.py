from .UUIDColumn import UUIDFKey
from sqlalchemy import Column, DateTime, Boolean, ForeignKey
from .BaseModel import BaseModel
from sqlalchemy.orm import relationship

class StudentAdmissionModel(BaseModel):
    """
    Represents a student's admission entry, including the admission details and user association.
    """
    __tablename__ = "student_admissions"

    admission_id = Column(ForeignKey("admissions.id"), index=True, comment="Foreign key referencing the related admission")
    admission = relationship("AdmissionModel", viewonly=True, uselist=False, lazy="joined")

    user_id = UUIDFKey("gql_ug.id", comment="Foreign key referencing the user associated with this admission")
    state_id = UUIDFKey(nullable=True, comment="State of the admission")

    extended_condition_date = Column(DateTime, nullable=True, comment="Date of extended condition")
    admissioned = Column(Boolean, default=False, comment="Bool if was admissioned")
    enrollment_date = Column(DateTime, comment="Date of entrollement")

    # exams = relationship("ExamModel", secondary="student_exam_links", uselist=True, lazy="joined")
