import strawberry
import uuid
import typing

import strawberry.types

StudentAdmissionGQLModel = typing.Annotated["StudentAdmissionGQLModel", strawberry.lazy(".StudentAdmissionGQLModel")]


@strawberry.federation.type(
    keys=["id"], extend=True, description="""An user in a system"""
)
class UserGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)

    from .BaseGQLModel import resolve_reference

    @strawberry.field(
        description="""List of student admissions related to the admission""",
        # permission_classes=[OnlyForAuthentized]
    )
    async def student_admissions(self, info: strawberry.types.Info) -> typing.List["StudentAdmissionGQLModel"]:
        from .StudentAdmissionGQLModel import StudentAdmissionGQLModel
        loader = StudentAdmissionGQLModel.getLoader(info)
        rows = await loader.filter_by(user_id=self.id)
        results = (StudentAdmissionGQLModel.from_dataclass(row) for row in rows)
        return results
