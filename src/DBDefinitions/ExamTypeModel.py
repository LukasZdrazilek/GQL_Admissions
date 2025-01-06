from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from .BaseModel import BaseModel
from uuid import UUID
import json

class ExamTypeModel(BaseModel):
    """
    Represents a type of exam associated with an admission, including metadata.
    """
    __tablename__ = "exam_types"

    name: Mapped[str] = mapped_column(nullable= True, default=None, comment="Name of the exam type")
    name_en: Mapped[str] = mapped_column(nullable= True, default=None, comment="English name of the exam type")

    min_score: Mapped[float] = mapped_column(nullable= True, default=None, comment="Minimum score of the exam type")
    max_score: Mapped[float] = mapped_column(nullable= True, default=None, comment="Maximum score of the exam type")
    score_table: Mapped[str] = mapped_column(nullable= True, default=None, comment="Score table of the exam type")

    admission_id: Mapped[UUID] = mapped_column(ForeignKey("admissions.id"), index=True, nullable=True, default=None, comment="Foreign key referencing the related admission")
    admission = relationship("AdmissionModel", viewonly=True, lazy="joined")
