from sqlalchemy import Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from .BaseModel import BaseModel
import uuid
from .UUIDColumn import UUIDFKey

class StudentAdmissionModel(BaseModel):
    """
    Represents a student's admission entry, including the admission details and user association.
    """
    __tablename__ = "student_admissions"

    admission_id: Mapped[int] = mapped_column(ForeignKey("admissions.id"), default=None, nullable=True, index=True, comment="Foreign key referencing the related admission")

    student_id: Mapped[uuid.UUID] = UUIDFKey("users.id", comment="Foreign key referencing to the student (user) associated with this admission")
    state_id: Mapped[uuid.UUID] = UUIDFKey("states.id",nullable=True, comment="State of the admission")

    extended_condition_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True, default=None, comment="Date of extended condition")
    admissioned: Mapped[bool] = mapped_column(Boolean, default=None, nullable=True, comment="Indicates if the student has been admitted")
    enrollment_date: Mapped[DateTime] = mapped_column(DateTime, default=None, nullable=True, comment="Date of enrollment")

    admission = relationship("AdmissionModel", viewonly=True, uselist=False, lazy="joined")

