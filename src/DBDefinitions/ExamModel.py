from sqlalchemy import Column, DateTime, String, ForeignKey
from .BaseModel import BaseModel
from sqlalchemy.orm import relationship

class ExamModel(BaseModel):
    """
    Represents an actual exam on certain date
    """
    __tablename__ = "exams"

    name = Column(String, comment="Name of the exam type")
    name_en = Column(String, comment="English name of the exam type")

    date = Column(DateTime, comment="Date of exam")

    exam_type_id = Column(ForeignKey('exam_types.id'), nullable=False, comment="Foreign key to exam type")
    exam_type = relationship('ExamTypeModel', viewonly=True, uselist=False, lazy='joined')

    exam_results = relationship('ExamResultModel')
    
