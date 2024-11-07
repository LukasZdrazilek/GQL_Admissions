from .UUIDColumn import UUIDColumn, UUIDFKey
from sqlalchemy import Column, DateTime, String, Boolean, ForeignKey
from .BaseModel import BaseModel
from sqlalchemy.orm import relationship
import sqlalchemy

from .BaseModel import BaseModel

class AdmissionModel(BaseModel):
    """
    Represents an admission entry for a specific course with associated metadata.
    """
    __tablename__ = "admissions"

    id = UUIDColumn()

    name = Column(String, comment="Name of the admission entry")
    name_en = Column(String, comment="English name of the admission entry")

    state_id = UUIDFKey(nullable=True, comment="stav přijímacího řízení")
    program_id = UUIDFKey(nullable=True, comment="Foreign key referencing the associated course")

    application_start_date = Column(DateTime, comment="Od kdy lze podat prihlasku")
    application_last_date = Column(DateTime, comment="Do kdy lze podat prihlasku")

    end_date = Column(DateTime, comment="Admission validity end date")

    condition_date = Column(DateTime, comment="Do kdy dolozit pozadavky")
    request_condition_start_date = Column(DateTime, comment="Od kdy mozne zadat o prodlouzeni")
    request_condition_last_date = Column(DateTime, comment="Do kdz mozne zadat o prodlouzeni")

    request_exam_start_date = Column(DateTime, comment="Od kdy mozne podat zadost o nahradni termin")
    request_exam_last_date = Column(DateTime, comment="Do kdy mozne podat zadost o nahradni termin")

    payment_date = Column(DateTime, comment="")

    request_enrollment_start_date = Column(DateTime, comment="From when its possible to ask for different date of enrollment")
    request_enrollment_end_date = Column(DateTime, comment="To when its possible to ask for different date of enrollment")

    student_admissions = relationship("StudentAdmissionModel", back_populates="admission")
    exam_types = relationship("ExamTypeModel", back_populates="admission")

    valid = Column(Boolean, default=True, comment="Indicates if the admission entry is valid")
