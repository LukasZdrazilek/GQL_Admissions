import dataclasses
from strawberry.scalars import JSON
import json

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
        description="Name of the exam type"
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="English name of the exam type"
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    min_score: typing.Optional[float] = strawberry.field(
        default=None,
        description="Minimum score for this exam type"
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    max_score: typing.Optional[float] = strawberry.field(
        default=None,
        description="Maximum score for this exam type"
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    admission_id: uuid.UUID = strawberry.field(
        description="The ID of the associated admission"
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    admission: typing.Optional["AdmissionGQLModel"] = strawberry.field(
        description="""The admission to which ExamType belongs""",
        resolver=ScalarResolver['AdmissionGQLModel'](fkey_field_name="admission_id"),
        # permission_classes=[
        #     OnlyForAuthentized
        # ],
    )

    exams: typing.List["ExamGQLModel"] = strawberry.field(
        description="""Exams of corresponding exam type""",
        resolver=VectorResolver["ExamGQLModel"](fkey_field_name="exam_type_id", whereType=None),
        # permission_classes = [
        #     OnlyForAuthentized,
        # ]
    )


@createInputs
@dataclasses.dataclass
class ExamTypeWhereFilter:
    id: uuid.UUID
    name: str
    name_en: str
    unified_id: uuid.UUID

exam_type_by_id = strawberry.field(
    description="Returns an Exam Type by id",
    # permission_classes=[OnlyForAuthentized],
    graphql_type=typing.Optional[ExamTypeGQLModel],
    resolver=ExamTypeGQLModel.load_with_loader
)

exam_type_page = strawberry.field(
    description="""Returns a list of exam types""",
    # permission_classes=[OnlyForAuthentized],
    resolver=PageResolver[ExamTypeGQLModel](whereType=ExamTypeWhereFilter)
)

########################################################################################################################
#                                                                                                                      #
#                                                    Mutations                                                         #
#                                                                                                                      #
########################################################################################################################

@strawberry.input(description="""Definition of an exam type used for creation""")
class ExamTypeInsertGQLModel:
    id: uuid.UUID = strawberry.field()
    name: typing.Optional[str] = strawberry.field(description="Name of the exam type", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the exam type", default=None)
    min_score: typing.Optional[float] = strawberry.field(description="Minimum score for this exam type", default=None)
    max_score: typing.Optional[float] = strawberry.field(description="Maximum score for this exam type", default=None)
    score_table: typing.Optional[JSON] = strawberry.field(description="The table of data of the exam type", default=None)
    admission_id: uuid.UUID = strawberry.field(description="The ID of the associated admission")

@strawberry.input(description="""Definition of an exam type used for creation""")
class ExamTypeUpdateGQLModel:
    id: uuid.UUID = strawberry.field()
    name: typing.Optional[str] = strawberry.field(description="Name of the exam type", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the exam type", default=None)
    min_score: typing.Optional[float] = strawberry.field(description="Minimum score for this exam type", default=None)
    max_score: typing.Optional[float] = strawberry.field(description="Maximum score for this exam type", default=None)
    score_table: typing.Optional[JSON] = strawberry.field(description="The table of data of the exam type",default=None)
    admission_id: uuid.UUID = strawberry.field(description="The ID of the associated admission")

@strawberry.input(description="""Definition of an exam type used for creation""")
class ExamTypeDeleteGQLModel:
    id: uuid.UUID = strawberry.field()
    name: typing.Optional[str] = strawberry.field(description="Name of the exam type", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the exam type", default=None)
    min_score: typing.Optional[float] = strawberry.field(description="Minimum score for this exam type", default=None)
    max_score: typing.Optional[float] = strawberry.field(description="Maximum score for this exam type", default=None)
    score_table: typing.Optional[JSON] = strawberry.field(description="The table of data of the exam type",default=None)
    admission_id: uuid.UUID = strawberry.field(description="The ID of the associated admission")

@strawberry.type(description="Result of a mutation for an exam type")
class ExamTypeMutationResultGQLModel:
    id: uuid.UUID = strawberry.field(description="The ID of the exam type", default=None)
    msg: str = strawberry.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberry.field(description="Returns the exam type")
    async def exam_type(self, info: strawberry.types.Info) -> typing.Union[ExamTypeGQLModel, None]:
        result = await ExamTypeGQLModel.resolve_reference(info, self.id)
        return result

########################################################################################################################

from uoishelpers.resolvers import Insert, InsertError
@strawberry.mutation(description="Adds a new exam type using stefek magic.")
async def exam_type_insert(self, info: strawberry.types.Info, exam_type: ExamTypeInsertGQLModel) -> typing.Union[ExamTypeGQLModel, InsertError[ExamTypeGQLModel]]:
    result = await Insert[ExamTypeGQLModel].DoItSafeWay(info=info, entity=exam_type)
    return result

from uoishelpers.resolvers import Update, UpdateError
@strawberry.mutation(description="Updates an exam type using stefek magic.")
async def exam_type_update(self, info: strawberry.types.Info, exam_type: ExamTypeUpdateGQLModel) -> typing.Union[ExamTypeGQLModel, UpdateError[ExamTypeGQLModel]]:
    result = await Update[ExamTypeGQLModel].DoItSafeWay(info=info, entity=exam_type)
    return result

from uoishelpers.resolvers import Delete, DeleteError
@strawberry.mutation(description="Deletes exam type using stefek magic.")
async def exam_type_delete(self, info: strawberry.types.Info, exam_type: ExamTypeDeleteGQLModel) -> typing.Union[ExamTypeGQLModel, DeleteError[ExamTypeGQLModel]]:
    result = await Delete[ExamTypeGQLModel].DoItSafeWay(info=info, entity=exam_type)
    return result