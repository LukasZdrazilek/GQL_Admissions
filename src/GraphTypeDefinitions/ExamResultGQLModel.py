import asyncio
import dataclasses
import datetime
import typing
import strawberry
import uuid

from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
    SimpleInsertPermission,
    SimpleUpdatePermission,
    SimpleDeletePermission
)
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
    ScalarResolver,
)


from .BaseGQLModel import BaseGQLModel

ExamGQLModel = typing.Annotated["ExamGQLModel", strawberry.lazy(".ExamGQLModel")]
StudentAdmissionGQLModel = typing.Annotated["StudentAdmissionGQLModel", strawberry.lazy(".StudentAdmissionGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Represents an exam result entry associated with an exam and a student admission."""
)
class ExamResultGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).ExamResultModel

    score: typing.Optional[float] = strawberry.field(
        default=None,
        description="Score achieved in the exam result"
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    exam_id: uuid.UUID = strawberry.field(
        default=None,
        description="The ID of the associated exam"
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    student_admission_id: uuid.UUID = strawberry.field(
        default=None,
        description="The ID of the related student admission"
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    exam: typing.Optional["ExamGQLModel"] = strawberry.field(
        description="""Exam associated with result""",
        resolver=ScalarResolver['ExamGQLModel'](fkey_field_name="exam_id"),
        # permission_classes=[
        #     OnlyForAuthentized
        # ],
    )

    student_admission: typing.Optional["StudentAdmissionGQLModel"] = strawberry.field(
        description="""Student admission associated with result""",
        resolver=ScalarResolver['StudentAdmissionGQLModel'](fkey_field_name="student_admission_id"),
        # permission_classes=[
        #     OnlyForAuthentized
        # ],
    )

@createInputs
@dataclasses.dataclass
class ExamResultInputFilter:
    id: uuid.UUID

exam_result_by_id = strawberry.field(
    description="Finds an exam result by ID",
    # permission_classes=[OnlyForAuthentized],
    graphql_type=typing.Optional[ExamResultGQLModel],
    resolver=ExamResultGQLModel.load_with_loader
)

exam_result_page = strawberry.field(
    description="Returns a list of exam results",
    # permission_classes=[OnlyForAuthentized],
    resolver=PageResolver[ExamResultGQLModel](whereType=ExamResultInputFilter)
)

########################################################################################################################
#                                                                                                                      #
#                                                    Mutations                                                         #
#                                                                                                                      #
########################################################################################################################

@strawberry.input(description="""Definition of an ExamResult used for creation""")
class ExamResultInsertGQLModel:
    id: typing.Optional[uuid.UUID] = strawberry.field()
    score: typing.Optional[float] = strawberry.field(description="Score achieved in the exam result")
    exam_id: uuid.UUID = strawberry.field(description="The ID of the associated exam")
    student_admission_id: uuid.UUID = strawberry.field(description="The ID of the related student admission")

@strawberry.input(description="""Definition of an ExamResult used for creation""")
class ExamResultUpdateGQLModel:
    id: typing.Optional[uuid.UUID] = strawberry.field()
    score: typing.Optional[float] = strawberry.field(description="Score achieved in the exam result")
    exam_id: uuid.UUID = strawberry.field(description="The ID of the associated exam")
    student_admission_id: uuid.UUID = strawberry.field(description="The ID of the related student admission")

@strawberry.input(description="""Definition of an ExamResult used for creation""")
class ExamResultDeleteGQLModel:
    id: typing.Optional[uuid.UUID] = strawberry.field()
    score: typing.Optional[float] = strawberry.field(description="Score achieved in the exam result")
    exam_id: uuid.UUID = strawberry.field(description="The ID of the associated exam")
    student_admission_id: uuid.UUID = strawberry.field(description="The ID of the related student admission")

@strawberry.type(description="Result of a mutation for an exam result")
class ExamResultMutationResultGQLModel:
    id: uuid.UUID = strawberry.field(description="The ID of the exam result", default=None)
    msg: str = strawberry.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberry.field(description="Returns the exam result")
    async def exam_result(self, info: strawberry.types.Info) -> typing.Union[ExamResultGQLModel, None]:
        result = await ExamResultGQLModel.resolve_reference(info, self.id)
        return result

########################################################################################################################

from uoishelpers.resolvers import Insert, InsertError
@strawberry.mutation(description="Adds a new exam result using stefek magic.")
async def exam_result_insert(self, info: strawberry.types.Info, exam_result: ExamResultInsertGQLModel) -> typing.Union[ExamResultGQLModel, InsertError[ExamResultGQLModel]]:
    result = await Insert[ExamResultGQLModel].DoItSafeWay(info=info, entity=exam_result)
    return result

from uoishelpers.resolvers import Update, UpdateError
@strawberry.mutation(description="Updates an exam result using stefek magic.")
async def exam_result_update(self, info: strawberry.types.Info, exam_result: ExamResultUpdateGQLModel) -> typing.Union[ExamResultGQLModel, UpdateError[ExamResultGQLModel]]:
    result = await Update[ExamResultGQLModel].DoItSafeWay(info=info, entity=exam_result)
    return result

from uoishelpers.resolvers import Delete, DeleteError
@strawberry.mutation(description="Deletes exam result using stefek magic.")
async def exam_result_delete(self, info: strawberry.types.Info, exam_result: ExamResultDeleteGQLModel) -> typing.Union[ExamResultGQLModel, DeleteError[ExamResultGQLModel]]:
    result = await Delete[ExamResultGQLModel].DoItSafeWay(info=info, entity=exam_result)
    return result