from .UUIDColumn import UUIDColumn, UUIDFKey
from sqlalchemy import Column, DateTime, String, Boolean, Integer, ForeignKey
from .BaseModel import BaseModel
from sqlalchemy.orm import relationship
import sqlalchemy

class DisciplineTypeModel(BaseModel):
    """
    Represents a type of discipline related to an exam type, with scoring and other metadata.
    """
    __tablename__ = "disciplinetypes"

    id = UUIDColumn()

    name = Column(String, comment="Name of the discipline type")
    name_en = Column(String, comment="English name of the discipline type")

    examtype_id = Column(ForeignKey("examtypes.id"), index=True, comment="Foreign key referencing the associated exam type")
    examtype = relationship("ExamTypeModel", back_populates="disciplinetypes")

    min_score = Column(Integer, comment="Minimum score required for this discipline")
    max_score = Column(Integer, comment="Maximum score achievable in this discipline")

    disciplines = relationship("DisciplineModel", back_populates="disciplinetype")

    valid = Column(Boolean, default=True, comment="Indicates if the discipline type is valid")
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when the discipline type was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last modification")
    createdby = UUIDFKey(nullable=True, comment="User ID of the creator")
    changedby = UUIDFKey(nullable=True, comment="User ID of the last modifier")
    rbacobject = UUIDFKey(nullable=True, comment="User or group ID that controls access to the discipline type")
