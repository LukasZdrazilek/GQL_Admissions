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

StudentAdmissionGQLModel = typing.Annotated["StudentAdmissionGQLModel", strawberry.lazy(".StudentAdmissionGQLModel")]
ExamResultGQLModel = typing.Annotated["ExamResultGQLModel", strawberry.lazy(".ExamResultGQLModel")]
ExamTypeGQLModel = typing.Annotated["ExamTypeGQLModel", strawberry.lazy(".ExamTypeGQLModel")]
FacilityGQLModel = typing.Annotated["FacilityGQLModel", strawberry.lazy(".FacilityGQLModel")]
GroupGQLModel = typing.Annotated["GroupGQLModel", strawberry.lazy(".GroupGQLModel")]


@strawberry.federation.type(
    keys=["id"], description="""Represents an actual exam on a certain date"""
)
class ExamGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).ExamModel

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

    exam_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="Date of the exam",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    examiners_id: typing.Optional[uuid.UUID] = strawberry.field(
        default=None,
        description="Foreign key referencing to group of examiners",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    facility_id: typing.Optional[uuid.UUID] = strawberry.field(
        default=None,
        description="Foreign key referencing to facility of exam",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    exam_type_id: uuid.UUID = strawberry.field(
        description="Foreign key to exam type",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    facility: typing.Optional["FacilityGQLModel"] = strawberry.field(
        description="""Facility associated with this exam""",
        resolver=ScalarResolver['FacilityGQLModel'](fkey_field_name="facility_id"),
        permission_classes=[
            OnlyForAuthentized,
        ],
    )

    examiners: typing.Optional["GroupGQLModel"] = strawberry.field(
        description="""Examiners associated with this exam""",
        resolver=ScalarResolver['GroupGQLModel'](fkey_field_name="examiners_id"),
        permission_classes=[
            OnlyForAuthentized,
        ],
    )

    exam_type: typing.Optional["ExamTypeGQLModel"] = strawberry.field(
        description="""Type of the exam""",
        resolver=ScalarResolver['ExamTypeGQLModel'](fkey_field_name="exam_type_id"),
        permission_classes=[
            OnlyForAuthentized,
        ],
    )

    exam_results: typing.List["ExamResultGQLModel"] = strawberry.field(
        description="""Results of the exam""",
        resolver=VectorResolver["ExamResultGQLModel"](fkey_field_name="exam_id", whereType=None),
        permission_classes = [
            OnlyForAuthentized,
        ]
    )

@createInputs
@dataclasses.dataclass
class ExamInputFilter:
    id: uuid.UUID
    name: str
    name_en: str
    exam_date: datetime.datetime
    exam_type_id: uuid.UUID
    examiners_id: uuid.UUID
    facility_id: uuid.UUID

exam_by_id = strawberry.field(
    description = """Finds an Exam by its id""",
    graphql_type=typing.Optional[ExamGQLModel],
    resolver=ExamGQLModel.load_with_loader,
    permission_classes=[
        OnlyForAuthentized,
    ]
)

exam_page = strawberry.field(
    description="""Returns a list of exams""",
    resolver=PageResolver[ExamGQLModel](whereType=ExamInputFilter),
    permission_classes=[
        OnlyForAuthentized,
    ],
)


########################################################################################################################
#                                                                                                                      #
#                                                    Mutations                                                         #
#                                                                                                                      #
########################################################################################################################

@strawberry.input(description="Definition of an exam used for creation")
class ExamInsertGQLModel:
    name: str = strawberry.field(description="Name of the exam type")
    exam_type_id: uuid.UUID = strawberry.field(description="Foreign key to exam type")

    id: typing.Optional[uuid.UUID] = strawberry.field(description="Primary key", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the exam type", default=None)
    exam_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of the exam", default=None)
    examiners_id: typing.Optional[uuid.UUID] = strawberry.field(description="Foreign key to group of examiners", default=None)
    facility_id: typing.Optional[uuid.UUID] = strawberry.field(description="Foreign key referencing to facility", default=None)

    rbacobject_id: typing.Optional[uuid.UUID] = strawberry.field(description="group_id or user_id defines access rights", default=None)
    createdby_id: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="Definition of an exam used for creation")
class ExamUpdateGQLModel:
    id: uuid.UUID = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Last change of the record")

    name: typing.Optional[str] = strawberry.field(description="Name of the exam type", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the exam type", default=None)
    exam_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of the exam", default=None)
    examiners_id: typing.Optional[uuid.UUID] = strawberry.field(description="Foreign key to group of examiners", default=None)
    facility_id: typing.Optional[uuid.UUID] = strawberry.field(description="Foreign key referencing to facility",default=None)
    exam_type_id: typing.Optional[uuid.UUID] = strawberry.field(description="Foreign key to exam type", default=None)

    changedby_id: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="Definition of an exam used for creation")
class ExamDeleteGQLModel:
    id: uuid.UUID = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Last change of the record")

########################################################################################################################

@strawberry.mutation(
    description="Adds a new admission using stefek magic.",
    permission_classes=[
        OnlyForAuthentized,
        SimpleInsertPermission[ExamGQLModel](roles=["administrátor", "administrátor přijímacího řízení"])
    ]
)
async def exam_insert(self, info: strawberry.types.Info, exam: ExamInsertGQLModel) -> typing.Union[ExamGQLModel, InsertError[ExamGQLModel]]:
    exam.rbacobject_id = exam.rbacobject_id # if admission.rbacobject_id else admission.group_id
    return await Insert[ExamGQLModel].DoItSafeWay(info=info, entity=exam)


@strawberry.mutation(
    description="Updates an admission using stefek magic.",
    permission_classes=[
        OnlyForAuthentized,
        SimpleUpdatePermission[ExamGQLModel](roles=["administrátor", "administrátor přijímacího řízení"])
    ]
)
async def exam_update(self, info: strawberry.types.Info, exam: typing.Annotated[ExamUpdateGQLModel, strawberry.argument(description="desc")]) -> typing.Union[ExamGQLModel, UpdateError[ExamGQLModel]]:
    return await Update[ExamGQLModel].DoItSafeWay(info=info, entity=exam)



@strawberry.mutation(
    description="Deletes admission using stefek magic.",
    permission_classes=[
        OnlyForAuthentized,
        SimpleDeletePermission[ExamGQLModel](roles=["administrátor", "administrátor přijímacího řízení"])
    ]
)
async def exam_delete(self, info: strawberry.types.Info, exam: ExamDeleteGQLModel) -> typing.Optional[DeleteError[ExamGQLModel]]:
    return await Delete[ExamGQLModel].DoItSafeWay(info=info, entity=exam)
