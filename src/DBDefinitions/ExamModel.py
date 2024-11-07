from .UUIDColumn import UUIDColumn, UUIDFKey
from sqlalchemy import Column, DateTime, String, Boolean, ForeignKey
from .BaseModel import BaseModel
from sqlalchemy.orm import relationship
import sqlalchemy

from .BaseModel import BaseModel

class ExamModel(BaseModel):
    """
    Represents an actual exam on certain date
    """
    __tablename__ = 'exams'

    id = UUIDColumn()

    name = Column(String, comment="Name of the exam type")
    name_en = Column(String, comment="English name of the exam type")

    date = Column(DateTime, comment="Date of exam")

    exam_type_id = Column(ForeignKey('exam_types.id'), nullable=False, comment="Foreign key to exam type")
    exam_type = relationship('ExamTypeModel', viewonly=True, uselist=False, lazy='joined')

    exam_results = relationship('ExamResultModel', back_populates='exam')

    valid = Column(Boolean, default=True, comment="Indicates if the exam type is valid")