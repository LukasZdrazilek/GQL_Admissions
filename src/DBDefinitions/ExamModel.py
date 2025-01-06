from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from datetime import datetime
from uuid import UUID

from .BaseModel import BaseModel
from .UUIDColumn import UUIDFKey

class ExamModel(BaseModel):
    """
    Represents an actual exam on a certain date.
    """
    __tablename__ = "exams"

    name: Mapped[str] = mapped_column(nullable=True, default=None, comment="Name of the exam type")
    name_en: Mapped[str] = mapped_column(nullable=True, default=None, comment="English name of the exam type")

    exam_date: Mapped[datetime] = mapped_column(nullable=True, default=None, comment="Date of exam")

    exam_type_id: Mapped[UUID] = mapped_column(ForeignKey('exam_types.id'), index=True, nullable=True, default=None, comment="Foreign key to exam type")

    examiners_id: Mapped[UUID] = UUIDFKey("", comment="Foreign key referencing the group of examiners associated with this exam")

    exam_type = relationship("ExamTypeModel", viewonly=True, lazy="joined")