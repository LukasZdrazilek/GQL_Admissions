import strawberry
import uuid
import typing

import strawberry.types

from uoishelpers.resolvers import VectorResolver

StudentAdmissionGQLModel = typing.Annotated["StudentAdmissionGQLModel", strawberry.lazy(".StudentAdmissionGQLModel")]


@strawberry.federation.type(
    keys=["id"], extend=True, description="""An user in a system"""
)
class UserGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)

    from .BaseGQLModel import resolve_reference

    student_admissions: typing.List["StudentAdmissionGQLModel"] = strawberry.field(
        description="""List of student admissions related to the admission""",
        resolver=VectorResolver["StudentAdmissionGQLModel"](fkey_field_name="student_id", whereType=None),
        # permission_classes = [
        #     OnlyForAuthentized,
        # ]
    )
