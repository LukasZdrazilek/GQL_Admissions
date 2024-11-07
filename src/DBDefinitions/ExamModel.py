from .UUIDColumn import UUIDColumn, UUIDFKey
from sqlalchemy import Column, DateTime, String, Boolean, ForeignKey
from .BaseModel import BaseModel
from sqlalchemy.orm import relationship
import sqlalchemy

class ExamModel(BaseModel):
    """
    Represents an actual exam on certain date
    """
    __tablename__ = 'exams'

    id = UUIDColumn()

    name = Column(String, comment="Name of the exam type")
    name_en = Column(String, comment="English name of the exam type")

    date = Column(DateTime, comment="Date of exam")

    # exam_type_id = Column(ForeignKey('exam_types.id'), nullable=False, comment="Foreign key to exam type")
    # exam_type = relationship('ExamTypeModel', viewonly=True, uselist=False, lazy='joined')
    #
    # exam_results = relationship('ExamResultModel', back_populates='exam')

    valid = Column(Boolean, default=True, comment="Indicates if the exam type is valid")
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when the exam type was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last modification")
    createdby = UUIDFKey(nullable=True, comment="User ID of the creator")
    changedby = UUIDFKey(nullable=True, comment="User ID of the last modifier")
    rbacobject = UUIDFKey(nullable=True, comment="User or group ID that controls access to the exam type")