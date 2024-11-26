from uuid import uuid4
from sqlalchemy import Column, Uuid

uuid = uuid4

def UUIDFKey(nullable=True, **kwargs):
    return Column(Uuid, index=True, nullable=nullable, **kwargs)

def UUIDColumn():
    return Column(Uuid, primary_key=True, comment="primary key", default=uuid)

def UnifiedUUIDColumn(**kwargs):
    return Column(Uuid, nullable=True, default=None, **kwargs)