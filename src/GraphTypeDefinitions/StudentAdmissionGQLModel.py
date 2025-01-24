import asyncio
import strawberry
import uuid
import datetime
import typing
import dataclasses

import strawberry.types
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
    ScalarResolver
)


from .BaseGQLModel import BaseGQLModel

AdmissionGQLModel = typing.Annotated["AdmissionGQLModel", strawberry.lazy(".AdmissionGQLModel")]
ExamGQLModel = typing.Annotated["ExamGQLModel", strawberry.lazy(".ExamGQLModel")]
ExamResultGQLModel = typing.Annotated["ExamResultGQLModel", strawberry.lazy(".ExamResultGQLModel")]
PaymentGQLModel = typing.Annotated["PaymentGQLModel", strawberry.lazy(".PaymentGQLModel")]
UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]
StateGQLModel = typing.Annotated["StateGQLModel", strawberry.lazy(".StateGQLModel")]

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
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    student_id: typing.Optional[uuid.UUID] = strawberry.field(
        default=None,
        description="""UUID of a student (user)""",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    state_id: typing.Optional[uuid.UUID] = strawberry.field(
        default=None,
        description="""UUID of a state""",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    extended_condition_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Date of extended condition""",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    admissioned: typing.Optional[bool] = strawberry.field(
        default=None,
        description="""True if an admissioned admission""",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    enrollment_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Date of enrollment""",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    payment_id: typing.Optional["uuid.UUID"] = strawberry.field(
        default=None,
        description="""UUID of a payment for admission""",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    payment: typing.Optional["PaymentGQLModel"] = strawberry.field(
        description="Payment for admission",
        resolver = ScalarResolver['PaymentGQLModel'](fkey_field_name="payment_id"),
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    admission: typing.Optional["AdmissionGQLModel"] = strawberry.field(
        description = "The admission to which Student Admission belongs",
        resolver = ScalarResolver['AdmissionGQLModel'](fkey_field_name = "admission_id"),
        permission_classes=[
            OnlyForAuthentized,
        ],
    )

    exam_results: typing.List["ExamResultGQLModel"] = strawberry.field(
        description="""Exam results related to the student admission""",
        resolver = VectorResolver["ExamResultGQLModel"](fkey_field_name = "student_admission_id", whereType = None),
        permission_classes = [
            OnlyForAuthentized,
        ]
    )

    student: typing.Optional["UserGQLModel"] = strawberry.field(
        description="""Student related to the admission""",
        resolver=ScalarResolver['UserGQLModel'](fkey_field_name="student_id"),
        permission_classes=[
            OnlyForAuthentized,
        ],
    )

    state: typing.Optional["StateGQLModel"] = strawberry.field(
        description="""State related to the admission""",
        resolver=ScalarResolver['StateGQLModel'](fkey_field_name="state_id"),
        permission_classes = [
            OnlyForAuthentized,
        ]
    )

@createInputs
@dataclasses.dataclass
class StudentAdmissionInputFilter:
    id: uuid.UUID
    admission_id: uuid.UUID
    student_id: uuid.UUID
    state_id: uuid.UUID
    extended_condition_date: datetime.datetime
    admissioned: bool
    enrollment_date: datetime.datetime
    payment_id: uuid.UUID

student_admission_by_id = strawberry.field(
    description="Returns a Student Admission by id",
    graphql_type=typing.Optional[StudentAdmissionGQLModel],
    resolver=StudentAdmissionGQLModel.load_with_loader,
    permission_classes=[
        OnlyForAuthentized
    ],
)

student_admission_page = strawberry.field(
    description="""Returns a list of student admissions""",
    resolver=PageResolver[StudentAdmissionGQLModel](whereType=StudentAdmissionInputFilter),
    permission_classes=[
        OnlyForAuthentized
    ],
)

########################################################################################################################
#                                                                                                                      #
#                                                    Mutations                                                         #
#                                                                                                                      #
########################################################################################################################

@strawberry.input(description="""Definition of an student admission used for creation""")
class StudentAdmissionInsertGQLModel:
    admission_id: uuid.UUID = strawberry.field(description="UUID of an admission")

    id: typing.Optional[uuid.UUID] = strawberry.field(description="Primary key", default=None)
    student_id: typing.Optional[uuid.UUID] = strawberry.field(description="UUID of a user", default=None)
    state_id: typing.Optional[uuid.UUID] = strawberry.field(description="UUID of a state", default=None)
    extended_condition_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of extended condition", default=None)
    admissioned: typing.Optional[bool] = strawberry.field(description="True if an admissioned admission", default=None)
    enrollment_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of enrollment", default=None)
    payment_id: typing.Optional[uuid.UUID] = strawberry.field(description="UUID of a payment", default=None)

    rbacobject_id: typing.Optional[uuid.UUID] = strawberry.field(description="group_id or user_id defines access rights", default=None)
    createdby_id: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="""Definition of an student admission used for creation""")
class StudentAdmissionUpdateGQLModel:
    id: uuid.UUID = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp")

    admission_id: typing.Optional[uuid.UUID] = strawberry.field(description="UUID of an admission", default=None)
    student_id: typing.Optional[uuid.UUID] = strawberry.field(description="UUID of a user", default=None)
    state_id: typing.Optional[uuid.UUID] = strawberry.field(description="UUID of a state", default=None)
    extended_condition_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of extended condition", default=None)
    admissioned: typing.Optional[bool] = strawberry.field(description="True if an admissioned admission", default=None)
    enrollment_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of enrollment", default=None)
    payment_id: typing.Optional[uuid.UUID] = strawberry.field(description="UUID of a payment", default=None)

    changedby_id: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="""Definition of an student admission used for creation""")
class StudentAdmissionDeleteGQLModel:
    id: typing.Optional[uuid.UUID] = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Last change of the record")


########################################################################################################################

@strawberry.mutation(
    description="Adds a new admission using stefek magic.",
    permission_classes=[
        OnlyForAuthentized,
        SimpleInsertPermission[StudentAdmissionGQLModel](roles=["administrátor", "administrátor přijímacího řízení"])
    ]
)
async def student_admission_insert(self, info: strawberry.types.Info, student_admission: StudentAdmissionInsertGQLModel) -> typing.Union[StudentAdmissionGQLModel, InsertError[StudentAdmissionGQLModel]]:
    student_admission.rbacobject_id = student_admission.rbacobject_id # if admission.rbacobject_id else admission.group_id
    return await Insert[StudentAdmissionGQLModel].DoItSafeWay(info=info, entity=student_admission)



@strawberry.mutation(
    description="Updates an admission using stefek magic.",
    permission_classes=[
        OnlyForAuthentized,
        SimpleUpdatePermission[StudentAdmissionGQLModel](roles=["administrátor", "administrátor přijímacího řízení"])
    ]
)
async def student_admission_update(self, info: strawberry.types.Info, student_admission: typing.Annotated[StudentAdmissionUpdateGQLModel, strawberry.argument(description="desc")]) -> typing.Union[StudentAdmissionGQLModel, UpdateError[StudentAdmissionGQLModel]]:
    return await Update[StudentAdmissionGQLModel].DoItSafeWay(info=info, entity=student_admission)



@strawberry.mutation(
    description="Deletes admission using stefek magic.",
    permission_classes=[
        OnlyForAuthentized,
        SimpleDeletePermission[StudentAdmissionGQLModel](roles=["administrátor", "administrátor přijímacího řízení"])
    ]
)
async def student_admission_delete(self, info: strawberry.types.Info, student_admission: StudentAdmissionDeleteGQLModel) -> typing.Optional[DeleteError[StudentAdmissionGQLModel]]:
    return await Delete[StudentAdmissionGQLModel].DoItSafeWay(info=info, entity=student_admission)