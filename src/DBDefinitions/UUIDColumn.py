from uuid import UUID
from sqlalchemy import Column, Uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import MappedAsDataclass, Mapped, mapped_column

def UUIDFKey(ForeignKeyArg=None, **kwargs):
    newkwargs = {
        **kwargs,
        "index": True,
        "primary_key": False,
        "default": None,
        "nullable": True,
        "comment": "foreign key"
    }
    return mapped_column(**newkwargs)

def UUIDColumn(**kwargs):
    newkwargs = {
        **kwargs,
        "index": True,
        "primary_key": True,
        "default_factory": UUID,
        "comment": "primary key"
    }
    return mapped_column(**newkwargs)