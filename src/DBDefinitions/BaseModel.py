import datetime
import sqlalchemy

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import MappedAsDataclass, Mapped, mapped_column

from .UUIDColumn import UUIDColumn, UUIDFKey
import uuid


class BaseModel(MappedAsDataclass, DeclarativeBase):
    id: Mapped[uuid.UUID] = UUIDColumn(index=True, primary_key=True, default_factory=uuid.uuid4)

    created: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True, server_default=sqlalchemy.sql.func.now(), comment="date time of creation")
    lastchange: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True, server_default=sqlalchemy.sql.func.now(), comment="date time stamp")

    createdby_id: Mapped[uuid.UUID] = UUIDFKey(ForeignKey("users.id"), comment="id of user who created this entity")
    changedby_id: Mapped[uuid.UUID] = UUIDFKey(ForeignKey("users.id"), comment="id of user who changed this entity")
    rbacobject_id: Mapped[uuid.UUID] = UUIDFKey(comment="id rbacobject")
