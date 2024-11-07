from email.policy import default

from .UUIDColumn import UUIDColumn, UUIDFKey
from sqlalchemy import Column, DateTime, String, Boolean, ForeignKey
from .BaseModel import BaseModel
from sqlalchemy.orm import relationship
import sqlalchemy

from .BaseModel import BaseModel

class StudentAdmissionModel(BaseModel):
    """
    Represents a student's admission entry, including the admission details and user association.
    """
    __tablename__ = "student_admissions"

    id = UUIDColumn()

    admission_id = Column(ForeignKey("admissions.id"), index=True, comment="Foreign key referencing the related admission")
    admission = relationship("AdmissionModel", back_populates="student_admissions")

    user_id = UUIDFKey("gql_ug.id", comment="Foreign key referencing the user associated with this admission")
    state_id = UUIDFKey(nullable=True, comment="stav přijímacího řízení")

    extended_condition = Column(Boolean, default=False, nullable=True, comment="Bool jestli ma student prodlouzeni")
    extended_condition_date = Column(DateTime, nullable=True, comment="Datum do kdy ma prodlouzeni")

    admissioned = Column(Boolean, default=False, comment="Bool if was admissioned")

    extended_enrollment = Column(Boolean, default=False, comment="Bool if was permitted to enroll on different date")
    enrollment_date = Column(DateTime, comment="Date of entrollement")
    enrolled = Column(Boolean, default=False, comment="Bool if was enrolled")


    valid = Column(Boolean, default=True, comment="Indicates if the student admission entry is valid")
