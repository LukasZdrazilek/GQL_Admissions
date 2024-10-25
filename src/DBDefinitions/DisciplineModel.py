from .UUIDColumn import UUIDColumn, UUIDFKey
from sqlalchemy import Column, DateTime, Boolean, Integer, ForeignKey
from .BaseModel import BaseModel
from sqlalchemy.orm import relationship
import sqlalchemy

class DisciplineModel(BaseModel):
    """
    Represents a discipline linked to a discipline type and an exam, including scoring and metadata.
    """
    __tablename__ = "disciplines"

    id = UUIDColumn()

    disciplinetype_id = Column(ForeignKey("disciplinetypes.id"), index=True, comment="Foreign key referencing the associated discipline type")
    disciplinetype = relationship("DisciplineTypeModel", back_populates="disciplines")

    exam_id = Column(ForeignKey("exams.id"), index=True, comment="Foreign key referencing the associated exam")
    exam = relationship("ExamModel", back_populates="disciplines")

    score = Column(Integer, comment="Score achieved in this discipline")

    valid = Column(Boolean, default=True, comment="Indicates if the discipline record is valid")
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when the discipline record was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last modification")
    createdby = UUIDFKey(nullable=True, comment="User ID of the creator")
    changedby = UUIDFKey(nullable=True, comment="User ID of the last modifier")
    rbacobject = UUIDFKey(nullable=True, comment="User or group ID that controls access to the discipline record")
