import strawberry
import uuid
import typing

import strawberry.types

from uoishelpers.resolvers import VectorResolver

ExamGQLModel = typing.Annotated["ExamGQLModel", strawberry.lazy(".ExamGQLModel")]

@strawberry.federation.type(
    keys=["id"], extend=True, description="""An group in a system"""
)
class GroupGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)

    from .BaseGQLModel import resolve_reference

    exams: typing.List["ExamGQLModel"] = strawberry.field(
        description="""List of exams related to the group""",
        resolver=VectorResolver["StudentAdmissionGQLModel"](fkey_field_name="examiners_id", whereType=None),
        # permission_classes = [
        #     OnlyForAuthentized,
        # ]
    )