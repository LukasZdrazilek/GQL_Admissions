from .UUIDColumn import UUIDColumn, UUIDFKey
from sqlalchemy import Column, DateTime, Boolean, ForeignKey
from .BaseModel import BaseModel
from sqlalchemy.orm import relationship
import sqlalchemy

class ExamModel(BaseModel):
    """
    Represents an exam entry associated with an exam type and a student admission.
    """
    __tablename__ = "exams"

    id = UUIDColumn()

    examtype_id = Column(ForeignKey("examtypes.id"), index=True, comment="Foreign key referencing the associated exam type")
    examtype = relationship("ExamTypeModel", back_populates="exams")

    admission_id = Column(ForeignKey("studentadmissions.id"), index=True, comment="Foreign key referencing the related student admission")

    valid = Column(Boolean, default=True, comment="Indicates if the exam entry is valid")
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when the exam was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last modification")
    createdby = UUIDFKey(nullable=True, comment="User ID of the creator")
    changedby = UUIDFKey(nullable=True, comment="User ID of the last modifier")
    rbacobject = UUIDFKey(nullable=True, comment="User or group ID that controls access to the exam entry")
