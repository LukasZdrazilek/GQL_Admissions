from .UUIDColumn import UUIDColumn, UUIDFKey
from sqlalchemy import Column, DateTime, String, Boolean, ForeignKey
from .BaseModel import BaseModel
from sqlalchemy.orm import relationship
import sqlalchemy

class StudentAdmissionModel(BaseModel):
    """
    Represents a student's admission entry, including the admission details and user association.
    """
    __tablename__ = "studentadmissions"

    id = UUIDColumn()

    admission_id = Column(ForeignKey("admissions.id"), index=True, comment="Foreign key referencing the related admission")
    admission = relationship("AdmissionModel", back_populates="admissions")

    user_id = UUIDFKey("gql_ug.id", comment="Foreign key referencing the user associated with this admission")
    state = Column(String, comment="Current state of the student's admission")

    valid = Column(Boolean, default=True, comment="Indicates if the student admission entry is valid")
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when the student admission entry was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last modification")
    createdby = UUIDFKey(nullable=True, comment="User ID of the creator")
    changedby = UUIDFKey(nullable=True, comment="User ID of the last modifier")
    rbacobject = UUIDFKey(nullable=True, comment="User or group ID that controls access to the student admission entry")
