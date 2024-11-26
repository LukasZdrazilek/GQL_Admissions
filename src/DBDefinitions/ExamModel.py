from sqlalchemy import Column, DateTime, String, ForeignKey
from .BaseModel import BaseModel
from sqlalchemy.orm import relationship
from .UUIDColumn import UnifiedUUIDColumn

class ExamModel(BaseModel):
    """
    Represents an actual exam on certain date
    """
    __tablename__ = "exams"

    name = Column(String, comment="Name of the exam type")
    name_en = Column(String, comment="English name of the exam type")

    exam_date = Column(DateTime, comment="Date of exam")

    exam_type_id = Column(ForeignKey('exam_types.id'), nullable=False, comment="Foreign key to exam type")
    exam_type = relationship('ExamTypeModel', viewonly=True, uselist=False, lazy='joined')

    unified_id = UnifiedUUIDColumn(comment="UUID used for unification of exams")

    # exam_results = relationship('ExamResultModel', back_populates='exam')
    # student_admissions = relationship('StudentAdmissionModel', secondary="student_exam_links", uselist=True, lazy="joined")
    