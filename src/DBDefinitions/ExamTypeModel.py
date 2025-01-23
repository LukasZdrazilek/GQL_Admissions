from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from .BaseModel import BaseModel
import uuid

class ExamTypeModel(BaseModel):
    r"""
    Represents a type of exam associated with an admission, including metadata.

    Master examType is a way to add a discipline, disciplineType respectively, without the need of adding additional database table.

    The background logic behind this is:
    Theoretical structure of ExamType, subExamType and Exam:

                                ExamType - Physical fitness test                                                  ExamType - Mathematics
                            /                   |                     \                                                    |
    subExamType - Sit-ups MEN       subExamType - Sit-ups WOMEN       subExamType - Twelve minute run                      |
                |                               |                                    |                                     |
 Exam - Sit-ups MEN 1. 4. 2025      Exam - Sit-ups WOMEN 1. 4. 2025      Exam - Twelve minute run 1. 4. 2025      Exam - Mathematics 3. 4. 2025


    """
    __tablename__ = "exam_types"

    name: Mapped[str] = mapped_column(nullable= True, default=None, comment="Name of the exam type")
    name_en: Mapped[str] = mapped_column(nullable= True, default=None, comment="English name of the exam type")

    min_score: Mapped[float] = mapped_column(nullable= True, default=None, comment="Minimum score of the exam type")
    max_score: Mapped[float] = mapped_column(nullable= True, default=None, comment="Maximum score of the exam type")

    master_exam_type_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("exam_types.id"), index=True, nullable=True, default=None, comment="UUID of the master exam type")
    admission_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("admissions.id"), index=True, nullable=True, default=None, comment="Foreign key referencing the related admission")

    master_exam_type = relationship("ExamTypeModel", viewonly=True)
    subexam_types = relationship("ExamTypeModel", remote_side="ExamTypeModel.id", viewonly=True, uselist=True)
    admission = relationship("AdmissionModel", viewonly=True, lazy="joined")
