import strawberry
import uuid
import typing

import strawberry.types

from uoishelpers.resolvers import VectorResolver

AdmissionGQLModel = typing.Annotated["AdmissionGQLModel", strawberry.lazy(".AdmissionGQLModel")]

@strawberry.federation.type(
    keys=["id"], extend=True, description="""Program in the system"""
)
class AcProgramGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)

    from .BaseGQLModel import resolve_reference

    admissions: typing.List["AdmissionGQLModel"] = strawberry.field(
        description = """List of admissions related to the program""",
        resolver = VectorResolver["AdmissionGQLModel"](fkey_field_name="program_id", whereType=None),
        # permission_classes = [
        #     OnlyForAuthentized,
        # ]
    )

