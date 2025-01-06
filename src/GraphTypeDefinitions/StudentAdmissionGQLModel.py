import asyncio
import strawberry
import uuid
import datetime
import typing
import dataclasses

import strawberry.types
from uoishelpers.gqlpermissions import OnlyForAuthentized

from uoishelpers.resolvers import (
    getLoadersFromInfo,
    createInputs,

    InsertError,
    Insert,
    UpdateError,
    Update,
    DeleteError,
    Delete,

    PageResolver,
    VectorResolver,
    ScalarResolver
)


from .BaseGQLModel import BaseGQLModel

AdmissionGQLModel = typing.Annotated["AdmissionGQLModel", strawberry.lazy(".AdmissionGQLModel")]
ExamGQLModel = typing.Annotated["ExamGQLModel", strawberry.lazy(".ExamGQLModel")]
ExamResultGQLModel = typing.Annotated["ExamResultGQLModel", strawberry.lazy(".ExamResultGQLModel")]
UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Entity representing a Student Admission"""
)
class StudentAdmissionGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).StudentAdmissionModel

    admission_id: uuid.UUID = strawberry.field(
        default=None,
        description="""UUID of an admission""",
        # permission_classes=[
        #   OnlyForAuthentized
        # ]
    )

    user_id: typing.Optional[uuid.UUID] = strawberry.field(
        default=None,
        description="""UUID of a user""",
        # permission_classes=[
        #   OnlyForAuthentized
        # ]
    )

    state_id: typing.Optional[uuid.UUID] = strawberry.field(
        default=None,
        description="""UUID of a state""",
        # permission_classes=[
        #   OnlyForAuthentized
        # ]
    )

    extended_condition_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Date of extended condition""",
        # permission_classes=[
        #   OnlyForAuthentized
        # ]
    )

    admissioned: typing.Optional[bool] = strawberry.field(
        default=None,
        description="""True if an admissioned admission""",
        # permission_classes=[
        #   OnlyForAuthentized
        # ]
    )

    enrollment_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Date of enrollment""",
        # permission_classes=[
        #   OnlyForAuthentized
        # ]
    )

    admission: typing.Optional["AdmissionGQLModel"] = strawberry.field(
        description = "The admission to which Student Admission belongs",
        resolver = ScalarResolver['AdmissionGQLModel'](fkey_field_name = "admission_id"),
        # permission_classes=[
        #     OnlyForAuthentized
        # ],
    )

    exam_results: typing.List["ExamResultGQLModel"] = strawberry.field(
        description="""Exam results related to the student admission""",
        resolver = VectorResolver["ExamResultGQLModel"](fkey_field_name = "student_admission_id", whereType = None),
        # permission_classes = [
        #     OnlyForAuthentized,
        # ]
    )

    @strawberry.field(description="Exams related to the student admission")
    async def exams(self, info: strawberry.types.Info) -> typing.Optional[typing.List["ExamGQLModel"]]:
        from .ExamGQLModel import ExamGQLModel
        loader = getLoadersFromInfo(info).student_exam_links
        rows = await loader.filter_by(student_id=self.id)
        awaitable = (ExamGQLModel.resolve_reference(info, row.exam_id) for row in rows)
        return await asyncio.gather(*awaitable)


    student: typing.Optional["UserGQLModel"] = strawberry.field(
        description="""Student related to the admission""",
        resolver=ScalarResolver['UserGQLModel'](fkey_field_name="user_id"),
        # permission_classes=[
        #     OnlyForAuthentized
        # ],
    )

@createInputs
@dataclasses.dataclass
class StudentAdmissionInputFilter:
    id: uuid.UUID

student_admission_by_id = strawberry.field(
    description="Returns a Student Admission by id",
    # permission_classes=[OnlyForAuthentized],  # Uncomment if needed
    graphql_type=typing.Union[StudentAdmissionGQLModel, None],
    resolver=StudentAdmissionGQLModel.resolve_reference
)

student_admission_page = strawberry.field(
    description="""Returns a list of student admissions""",
    # permission_classes=[OnlyForAuthentized],
    resolver=PageResolver[StudentAdmissionGQLModel](whereType=StudentAdmissionInputFilter)
)

########################################################################################################################
#                                                                                                                      #
#                                                    Mutations                                                         #
#                                                                                                                      #
########################################################################################################################

@strawberry.input(description="""Definition of an student admission used for creation""")
class StudentAdmissionInsertGQLModel:
    id: typing.Optional[uuid.UUID] = strawberry.field()
    admission_id: uuid.UUID = strawberry.field(description="UUID of an admission")
    user_id: typing.Optional[uuid.UUID] = strawberry.field(description="UUID of a user")
    state_id: typing.Optional[uuid.UUID] = strawberry.field(description="UUID of a state")
    extended_condition_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of extended condition")
    admissioned: typing.Optional[bool] = strawberry.field(description="True if an admissioned admission")
    enrollment_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of enrollment")

@strawberry.input(description="""Definition of an student admission used for creation""")
class StudentAdmissionUpdateGQLModel:
    id: uuid.UUID = strawberry.field()
    lastchange: datetime.datetime = strawberry.field(description="Timestamp")

    admission_id: typing.Optional[uuid.UUID] = strawberry.field(description="UUID of an admission", default=None)
    user_id: typing.Optional[uuid.UUID] = strawberry.field(description="UUID of a user", default=None)
    state_id: typing.Optional[uuid.UUID] = strawberry.field(description="UUID of a state", default=None)
    extended_condition_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of extended condition", default=None)
    admissioned: typing.Optional[bool] = strawberry.field(description="True if an admissioned admission", default=None)
    enrollment_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of enrollment", default=None)

@strawberry.input(description="""Definition of an student admission used for creation""")
class StudentAdmissionDeleteGQLModel:
    id: typing.Optional[uuid.UUID] = strawberry.field()
    admission_id: uuid.UUID = strawberry.field(description="UUID of an admission")
    user_id: typing.Optional[uuid.UUID] = strawberry.field(description="UUID of a user")
    state_id: typing.Optional[uuid.UUID] = strawberry.field(description="UUID of a state")
    extended_condition_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of extended condition")
    admissioned: typing.Optional[bool] = strawberry.field(description="True if an admissioned admission")
    enrollment_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of enrollment")    

@strawberry.type(description="Result of a mutation for a student admission")
class StudentAdmissionMutationResultGQLModel:
    id: uuid.UUID = strawberry.field(description="The ID of the student admission", default=None)
    msg: str = strawberry.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberry.field(description="Returns the student admission")
    async def student_admission(self, info: strawberry.types.Info) -> typing.Union[StudentAdmissionGQLModel, None]:
        result = await StudentAdmissionGQLModel.resolve_reference(info, self.id)
        return result

########################################################################################################################

@strawberry.mutation(description="Adds a new student admission using stefek magic.")
async def student_admission_insert(self, info: strawberry.types.Info, student_admission: StudentAdmissionInsertGQLModel) -> typing.Union[StudentAdmissionGQLModel, InsertError[StudentAdmissionGQLModel]]:
    result = await Insert[StudentAdmissionGQLModel].DoItSafeWay(info=info, entity=student_admission)
    return result

@strawberry.mutation(description="Updates new student admission using stefek magic.")
async def student_admission_update(self, info: strawberry.types.Info, student_admission: StudentAdmissionUpdateGQLModel) -> typing.Union[StudentAdmissionGQLModel, UpdateError[StudentAdmissionGQLModel]]:
    result = await Update[StudentAdmissionGQLModel].DoItSafeWay(info=info, entity=student_admission)
    return result

@strawberry.mutation(description="Deletes new student admission using stefek magic.")
async def student_admission_delete(self, info: strawberry.types.Info, student_admission: StudentAdmissionDeleteGQLModel) -> typing.Union[StudentAdmissionGQLModel, DeleteError[StudentAdmissionGQLModel]]:
    result = await Delete[StudentAdmissionGQLModel].DoItSafeWay(info=info, entity=student_admission)
    return result