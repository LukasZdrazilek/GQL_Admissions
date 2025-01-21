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
    ScalarResolver,
    VectorResolver,
)


from .BaseGQLModel import BaseGQLModel

AdmissionGQLModel = typing.Annotated["AdmissionGQLModel", strawberry.lazy(".AdmissionGQLModel")]
ExamGQLModel = typing.Annotated["ExamGQLModel", strawberry.lazy(".ExamGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Represents a type of exam associated with an admission, including metadata"""
)
class ExamTypeGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).ExamTypeModel

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="Name of the exam type",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="English name of the exam type",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    min_score: typing.Optional[float] = strawberry.field(
        default=None,
        description="Minimum score for this exam type",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    max_score: typing.Optional[float] = strawberry.field(
        default=None,
        description="Maximum score for this exam type",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    master_exam_type_id: typing.Optional[uuid.UUID] = strawberry.field(
        default=None,
        description="The ID of the examType that this examType belongs to",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    master_exam_type: typing.Optional["ExamTypeGQLModel"] = strawberry.field(
        description="The examType that this examType belongs to",
        resolver=ScalarResolver["ExamTypeGQLModel"](fkey_field_name="master_exam_type_id"),
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    sub_exam_types: typing.List["ExamTypeGQLModel"] = strawberry.field(
        description="ExamTypes that belong to this examType",
        resolver=VectorResolver["ExamTypeGQLModel"](fkey_field_name="master_exam_type_id", whereType=None),
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    admission_id: uuid.UUID = strawberry.field(
        description="The ID of the associated admission",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    admission: typing.Optional["AdmissionGQLModel"] = strawberry.field(
        description="""The admission to which ExamType belongs""",
        resolver=ScalarResolver['AdmissionGQLModel'](fkey_field_name="admission_id"),
        permission_classes=[
            OnlyForAuthentized
        ],
    )

    exams: typing.List["ExamGQLModel"] = strawberry.field(
        description="""Exams of corresponding exam type""",
        resolver=VectorResolver["ExamGQLModel"](fkey_field_name="exam_type_id", whereType=None),
        permission_classes = [
            OnlyForAuthentized,
        ]
    )


@createInputs
@dataclasses.dataclass
class ExamTypeWhereFilter:
    id: uuid.UUID
    name: str
    name_en: str
    min_score: float
    max_score: float
    master_exam_type_id: uuid.UUID
    admission_id: uuid.UUID

exam_type_by_id = strawberry.field(
    description="Returns an Exam Type by id",
    graphql_type=typing.Optional[ExamTypeGQLModel],
    resolver=ExamTypeGQLModel.load_with_loader,
    permission_classes=[
        OnlyForAuthentized,
    ],
)

exam_type_page = strawberry.field(
    description="""Returns a list of exam types""",
    resolver=PageResolver[ExamTypeGQLModel](whereType=ExamTypeWhereFilter),
    permission_classes=[
        OnlyForAuthentized,
    ]
)

########################################################################################################################
#                                                                                                                      #
#                                                    Mutations                                                         #
#                                                                                                                      #
########################################################################################################################

@strawberry.input(description="""Definition of an exam type used for creation""")
class ExamTypeInsertGQLModel:
    name: str = strawberry.field(description="Name of the exam type")
    admission_id: uuid.UUID = strawberry.field(description="The ID of the associated admission")

    id: typing.Optional[uuid.UUID] = strawberry.field(description="Primary key", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the exam type", default=None)
    min_score: typing.Optional[float] = strawberry.field(description="Minimum score for this exam type", default=None)
    max_score: typing.Optional[float] = strawberry.field(description="Maximum score for this exam type", default=None)
    master_exam_type_id: typing.Optional[uuid.UUID] = strawberry.field(description="The ID of the examType that this exam type belongs to", default=None)

    rbacobject_id: typing.Optional[uuid.UUID] = strawberry.field(description="group_id or user_id defines access rights", default=None)
    createdby_id: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="""Definition of an exam type used for creation""")
class ExamTypeUpdateGQLModel:
    id: uuid.UUID = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Last change of the record")

    name: typing.Optional[str] = strawberry.field(description="Name of the exam type", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the exam type", default=None)
    min_score: typing.Optional[float] = strawberry.field(description="Minimum score for this exam type", default=None)
    max_score: typing.Optional[float] = strawberry.field(description="Maximum score for this exam type", default=None)
    admission_id: typing.Optional[uuid.UUID] = strawberry.field(description="The ID of the associated admission", default=None)
    master_exam_type_id: typing.Optional[uuid.UUID] = strawberry.field(description="The ID of the examType that this exam type belongs to", default=None)

    changedby_id: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="""Definition of an exam type used for creation""")
class ExamTypeDeleteGQLModel:
    id: uuid.UUID = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Last change of the record")

########################################################################################################################

@strawberry.mutation(
    description="Adds a new admission using stefek magic.",
    permission_classes=[
        OnlyForAuthentized,
        SimpleInsertPermission[ExamTypeGQLModel](roles=["administrátor", "administrátor přijímacího řízení"])
    ]
)
async def exam_type_insert(self, info: strawberry.types.Info, exam_type: ExamTypeInsertGQLModel) -> typing.Union[ExamTypeGQLModel, InsertError[ExamTypeGQLModel]]:
    exam_type.rbacobject_id = exam_type.rbacobject_id # if admission.rbacobject_id else admission.group_id
    return await Insert[ExamTypeGQLModel].DoItSafeWay(info=info, entity=exam_type)



@strawberry.mutation(
    description="Updates an admission using stefek magic.",
    permission_classes=[
        OnlyForAuthentized,
        SimpleUpdatePermission[ExamTypeGQLModel](roles=["administrátor", "administrátor přijímacího řízení"])
    ]
)
async def exam_type_update(self, info: strawberry.types.Info, exam_type: typing.Annotated[ExamTypeUpdateGQLModel, strawberry.argument(description="desc")]) -> typing.Union[ExamTypeGQLModel, UpdateError[ExamTypeGQLModel]]:
    return await Update[ExamTypeGQLModel].DoItSafeWay(info=info, entity=exam_type)



@strawberry.mutation(
    description="Deletes admission using stefek magic.",
    permission_classes=[
        OnlyForAuthentized,
        SimpleDeletePermission[ExamTypeGQLModel](roles=["administrátor", "administrátor přijímacího řízení"])
    ]
)
async def exam_type_delete(self, info: strawberry.types.Info, exam_type: ExamTypeDeleteGQLModel) -> typing.Optional[DeleteError[ExamTypeGQLModel]]:
    return await Delete[ExamTypeGQLModel].DoItSafeWay(info=info, entity=exam_type)
