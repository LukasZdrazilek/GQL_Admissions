import strawberry
import uuid
import typing

import strawberry.types

from uoishelpers.resolvers import VectorResolver
from uoishelpers.gqlpermissions import OnlyForAuthentized

ExamGQLModel = typing.Annotated["ExamGQLModel", strawberry.lazy(".ExamGQLModel")]

@strawberry.federation.type(
    keys=["id"], extend=True, description="""A facility in a system"""
)
class FacilityGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)

    from .BaseGQLModel import resolve_reference

    exams: typing.List["ExamGQLModel"] = strawberry.field(
        description="""List of exams related to the facility""",
        resolver=VectorResolver["ExamGQLModel"](fkey_field_name="facility_id", whereType=None),
        permission_classes = [
            OnlyForAuthentized,
        ]
    )