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
        description="Score achieved in the exam result",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    exam_id: uuid.UUID = strawberry.field(
        default=None,
        description="The ID of the associated exam",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    student_admission_id: uuid.UUID = strawberry.field(
        default=None,
        description="The ID of the related student admission",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    exam: typing.Optional["ExamGQLModel"] = strawberry.field(
        description="""Exam associated with result""",
        resolver=ScalarResolver['ExamGQLModel'](fkey_field_name="exam_id"),
        permission_classes=[
            OnlyForAuthentized,
        ],
    )

    student_admission: typing.Optional["StudentAdmissionGQLModel"] = strawberry.field(
        description="""Student admission associated with result""",
        resolver=ScalarResolver['StudentAdmissionGQLModel'](fkey_field_name="student_admission_id"),
        permission_classes=[
            OnlyForAuthentized,
        ],
    )

@createInputs
@dataclasses.dataclass
class ExamResultInputFilter:
    id: uuid.UUID
    score: float
    exam_id: uuid.UUID
    student_admission_id: uuid.UUID

exam_result_by_id = strawberry.field(
    description="Finds an exam result by ID",
    graphql_type=typing.Optional[ExamResultGQLModel],
    resolver=ExamResultGQLModel.load_with_loader,
    permission_classes=[
        OnlyForAuthentized,
    ]
)

exam_result_page = strawberry.field(
    description="Returns a list of exam results",
    resolver=PageResolver[ExamResultGQLModel](whereType=ExamResultInputFilter),
    permission_classes=[
        OnlyForAuthentized,
    ]
)

########################################################################################################################
#                                                                                                                      #
#                                                    Mutations                                                         #
#                                                                                                                      #
########################################################################################################################

@strawberry.input(description="""Definition of an ExamResult used for creation""")
class ExamResultInsertGQLModel:
    exam_id: uuid.UUID = strawberry.field(description="The ID of the associated exam")
    student_admission_id: uuid.UUID = strawberry.field(description="The ID of the related student admission")

    id: typing.Optional[uuid.UUID] = strawberry.field(description="Primary key", default=None)
    score: typing.Optional[float] = strawberry.field(description="Score achieved in the exam result", default=None)

    rbacobject_id: typing.Optional[uuid.UUID] = strawberry.field(description="group_id or user_id defines access rights", default=None)
    createdby_id: strawberry.Private[uuid.UUID] = None


@strawberry.input(description="""Definition of an ExamResult used for creation""")
class ExamResultUpdateGQLModel:
    id: uuid.UUID = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Last change of the record")

    exam_id: typing.Optional[uuid.UUID] = strawberry.field(description="The ID of the associated exam", default=None)
    score: typing.Optional[float] = strawberry.field(description="Score achieved in the exam result", default=None)
    student_admission_id: typing.Optional[uuid.UUID] = strawberry.field(description="The ID of the related student admission", default=None)

    changedby_id: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="""Definition of an ExamResult used for creation""")
class ExamResultDeleteGQLModel:
    id: typing.Optional[uuid.UUID] = strawberry.field()
    lastchange: datetime.datetime = strawberry.field(description="Last change of the record")

########################################################################################################################

@strawberry.mutation(
    description="Adds a new admission using stefek magic.",
    permission_classes=[
        OnlyForAuthentized,
        SimpleInsertPermission[ExamResultGQLModel](roles=["administrátor", "administrátor přijímacího řízení"])
    ]
)
async def exam_result_insert(self, info: strawberry.types.Info, exam_result: ExamResultInsertGQLModel) -> typing.Union[ExamResultGQLModel, InsertError[ExamResultGQLModel]]:
    exam_result.rbacobject_id = exam_result.rbacobject_id # if admission.rbacobject_id else admission.group_id
    return await Insert[ExamResultGQLModel].DoItSafeWay(info=info, entity=exam_result)



@strawberry.mutation(
    description="Updates an admission using stefek magic.",
    permission_classes=[
        OnlyForAuthentized,
        SimpleUpdatePermission[ExamResultGQLModel](roles=["administrátor", "administrátor přijímacího řízení"])
    ]
)
async def exam_result_update(self, info: strawberry.types.Info, exam_result: typing.Annotated[ExamResultUpdateGQLModel, strawberry.argument(description="desc")]) -> typing.Union[ExamResultGQLModel, UpdateError[ExamResultGQLModel]]:
    return await Update[ExamResultGQLModel].DoItSafeWay(info=info, entity=exam_result)



@strawberry.mutation(
    description="Deletes admission using stefek magic.",
    permission_classes=[
        OnlyForAuthentized,
        SimpleDeletePermission[ExamResultGQLModel](roles=["administrátor", "administrátor přijímacího řízení"])
    ]
)
async def exam_result_delete(self, info: strawberry.types.Info, exam_result: ExamResultDeleteGQLModel) -> typing.Optional[DeleteError[ExamResultGQLModel]]:
    return await Delete[ExamResultGQLModel].DoItSafeWay(info=info, entity=exam_result)
