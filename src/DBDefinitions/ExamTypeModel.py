from .UUIDColumn import UUIDColumn, UUIDFKey
from sqlalchemy import Column, DateTime, String, Boolean, ForeignKey
from .BaseModel import BaseModel
from sqlalchemy.orm import relationship
import sqlalchemy

class ExamTypeModel(BaseModel):
    """
    Represents a type of exam associated with an admission, including metadata.
    """
    __tablename__ = "examtypes"

    id = UUIDColumn()
    
    name = Column(String, comment="Name of the exam type")
    name_en = Column(String, comment="English name of the exam type")

    admission_id = Column(ForeignKey("admissions.id"), index=True, comment="Foreign key referencing the associated admission")
    admission = relationship("AdmissionModel", back_populates="examtypes")

    exams = relationship("ExamModel", back_populates="examtype")

    valid = Column(Boolean, default=True, comment="Indicates if the exam type is valid")
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when the exam type was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last modification")
    createdby = UUIDFKey(nullable=True, comment="User ID of the creator")
    changedby = UUIDFKey(nullable=True, comment="User ID of the last modifier")
    rbacobject = UUIDFKey(nullable=True, comment="User or group ID that controls access to the exam type")
