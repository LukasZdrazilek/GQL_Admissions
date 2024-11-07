import sqlalchemy
import datetime

from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    DateTime,
    ForeignKey,
    Sequence,
    Table,
    Boolean,
    Uuid
)
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.hybrid import hybrid_property
from .UUIDColumn import UUIDColumn, UUIDFKey


class BaseModel(DeclarativeBase):
    id = UUIDColumn()

    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when the admission entry was created")
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last change to the admission entry")
    createdby_id = UUIDFKey(nullable=True, comment="User ID of the creator")#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby_id = UUIDFKey(nullable=True, comment="User ID of the last modifier")#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject_id = UUIDFKey(nullable=True, comment="User or group ID that controls access to the admission entry")#Column(ForeignKey("users.id"), index=True, nullable=True)
