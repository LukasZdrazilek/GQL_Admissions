import sqlalchemy

from sqlalchemy import (
    Column,
    DateTime,
    Boolean,
)

from sqlalchemy.orm import DeclarativeBase
from .UUIDColumn import UUIDColumn, UUIDFKey


class BaseModel(DeclarativeBase):
    id = UUIDColumn()

    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when the admission entry was created")
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last change to the admission entry")
    createdby_id = UUIDFKey(nullable=True, comment="User ID of the creator")#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby_id = UUIDFKey(nullable=True, comment="User ID of the last modifier")#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject_id = UUIDFKey(nullable=True, comment="User or group ID that controls access to the admission entry")#Column(ForeignKey("users.id"), index=True, nullable=True)

    valid = Column(Boolean, default=True, comment="Indicates if the exam entry is valid")