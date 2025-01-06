from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped
from uuid import UUID
from sqlalchemy import ForeignKey
from .UUIDColumn import UUIDFKey

from .BaseModel import BaseModel

class AdmissionModel(BaseModel):
    """
    Represents an admission entry for a specific course with associated metadata.
    """
    __tablename__ = "admissions"

    name: Mapped[str] = mapped_column(nullable= True, default=None, comment="Name of the admission entry")
    name_en: Mapped[str] = mapped_column(nullable= True, default=None, comment="English name of the admission entry")

    program_id: Mapped[UUID] = UUIDFKey("", comment="Foreign key referencing to program associated with this admission")

    application_start_date: Mapped[datetime] = mapped_column(nullable= True, default=None, comment="From when its possible to apply")
    application_last_date: Mapped[datetime] = mapped_column(nullable= True, default=None, comment="To when its possible to apply")

    end_date: Mapped[datetime] = mapped_column(nullable= True, default=None, comment="Admission validity end date")

    condition_date: Mapped[datetime] = mapped_column(nullable= True, default=None, comment="By when to document conditions")
    request_condition_start_date: Mapped[datetime] = mapped_column(nullable= True, default=None, comment="From when its possible to ask for extension")
    request_condition_last_date: Mapped[datetime] = mapped_column(nullable= True, default=None, comment="To when its possible to ask for extension")

    request_exam_start_date: Mapped[datetime] = mapped_column(nullable= True, default=None, comment="From when its possible to ask for different date of exam")
    request_exam_last_date: Mapped[datetime] = mapped_column(nullable= True, default=None, comment="To when its possible to ask for different date of exam")

    payment_date: Mapped[datetime] = mapped_column(nullable= True, default=None, comment="")

    request_enrollment_start_date: Mapped[datetime] = mapped_column(nullable= True, default=None, comment="From when its possible to ask for different date of enrollment")
    request_enrollment_end_date: Mapped[datetime] = mapped_column(nullable= True, default=None, comment="To when its possible to ask for different date of enrollment")
