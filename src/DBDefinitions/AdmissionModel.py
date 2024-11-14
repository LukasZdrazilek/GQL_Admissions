from .UUIDColumn import UUIDFKey
from sqlalchemy import Column, DateTime, String
from .BaseModel import BaseModel
from sqlalchemy.orm import relationship

class AdmissionModel(BaseModel):
    """
    Represents an admission entry for a specific course with associated metadata.
    """
    __tablename__ = "admissions"

    name = Column(String, comment="Name of the admission entry")
    name_en = Column(String, comment="English name of the admission entry")

    state_id = UUIDFKey(nullable=True, comment="State of the admission")
    program_id = UUIDFKey(nullable=True, comment="Foreign key referencing the associated course")

    application_start_date = Column(DateTime, comment="From when its possible to apply")
    application_last_date = Column(DateTime, comment="To when its possible to apply")

    end_date = Column(DateTime, comment="Admission validity end date")

    condition_date = Column(DateTime, comment="By when to document conditions")
    request_condition_start_date = Column(DateTime, comment="From when its possible to ask for extension")
    request_condition_last_date = Column(DateTime, comment="To when its possible to ask for extension")

    request_exam_start_date = Column(DateTime, comment="From when its possible to ask for different date of exam")
    request_exam_last_date = Column(DateTime, comment="To when its possible to ask for different date of exam")

    payment_date = Column(DateTime, comment="")

    request_enrollment_start_date = Column(DateTime, comment="From when its possible to ask for different date of enrollment")
    request_enrollment_end_date = Column(DateTime, comment="To when its possible to ask for different date of enrollment")

    student_admissions = relationship("StudentAdmissionModel", back_populates="admission")
    exam_types = relationship("ExamTypeModel", back_populates="admission")
