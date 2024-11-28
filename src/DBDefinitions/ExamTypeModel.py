from sqlalchemy import Column, String, ForeignKey, Float
from sqlalchemy.dialects.postgresql import HSTORE
from .BaseModel import BaseModel
from sqlalchemy.orm import relationship
from .UUIDColumn import UnifiedUUIDColumn

class ExamTypeModel(BaseModel):
    """
    Represents a type of exam associated with an admission, including metadata.
    """
    __tablename__ = "exam_types"
    
    name = Column(String, comment="Name of the exam type")
    name_en = Column(String, comment="English name of the exam type")

    min_score = Column(Float, comment="Minimum score of the exam type")
    max_score = Column(Float, comment="Maximum score of the exam type")

    data = Column(HSTORE, comment="Dictionary of an score table")

    unified_id = UnifiedUUIDColumn(comment="Unified ID of the exam type")
    unified_name = Column(String, nullable=True, default=None, comment="Unified name of the exam")
    unified_name_en = Column(String, nullable=True, default=None, comment="English unified name of the exam")

    admission_id = Column(ForeignKey("admissions.id"), nullable=False)
    admission = relationship("AdmissionModel", viewonly=True, uselist=False, lazy="joined")
