from .UUIDColumn import UUIDColumn, UUIDFKey
from sqlalchemy import Column, DateTime, String, Boolean, ForeignKey
from .BaseModel import BaseModel
from sqlalchemy.orm import relationship
import sqlalchemy

class AdmissionModel(BaseModel):
    """
    Represents an admission entry for a specific course with associated metadata.
    """
    __tablename__ = "admissions"

    id = UUIDColumn()
    name = Column(String, comment="Name of the admission entry")
    name_en = Column(String, comment="English name of the admission entry")

    #course_id = Column(ForeignKey("gql_granting.id"), index=True, comment="Foreign key referencing the associated course")
    course_id = UUIDFKey(nullable=True, comment="Foreign key referencing the associated course")

    startdate = Column(DateTime, comment="Admission validity start date")
    enddate = Column(DateTime, comment="Admission validity end date")

    admissions = relationship("AdmissionTypeModel", back_populates="admissiontype")

    valid = Column(Boolean, default=True, comment="Indicates if the admission entry is valid")
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when the admission entry was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last change to the admission entry")
    createdby = UUIDFKey(nullable=True, comment="User ID of the creator")
    changedby = UUIDFKey(nullable=True, comment="User ID of the last modifier")
    rbacobject = UUIDFKey(nullable=True, comment="User or group ID that controls access to the admission entry")
