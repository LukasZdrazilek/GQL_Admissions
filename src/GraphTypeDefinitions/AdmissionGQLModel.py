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
    ScalarResolver,
    VectorResolver,
)


from .BaseGQLModel import BaseGQLModel

StudentAdmissionGQLModel = typing.Annotated["StudentAdmissionGQLModel", strawberry.lazy(".StudentAdmissionGQLModel")]
ExamTypeGQLModel = typing.Annotated["ExamTypeGQLModel", strawberry.lazy(".ExamTypeGQLModel")]
AcProgramGQLModel = typing.Annotated["AcProgramGQLModel", strawberry.lazy(".AcProgramGQLModel")]
PaymentInfoGQLModel = typing.Annotated["PaymentInfoGQLModel", strawberry.lazy(".PaymentInfoGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Admission for corresponding year and program"""
)
class AdmissionGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).AdmissionModel

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Name of the admission entry""",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="""English name of the admission entry""",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    program_id: typing.Optional[uuid.UUID] = strawberry.field(
        default=None,
        description="""Foreign key referencing to the associated program""",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    application_start_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Od kdy lze podat přihlášku""",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    application_last_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Do kdy lze podat přihlášku""",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    end_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Admission validity end date""",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    condition_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Do kdy doložit požadavky""",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    request_condition_start_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Od kdy možné žádat o prodloužení""",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    request_condition_last_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Do kdy možné žádat o prodloužení""",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    request_exam_start_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Od kdy možné podat žádost o náhradní termín""",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    request_exam_last_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Do kdy možné podat žádost o náhradní termín""",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    payment_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Do kdy lze zaplatit poplatek""",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    payment_info_id: typing.Optional[uuid.UUID] = strawberry.field(
        default=None,
        description="""Foreign key referencing to the associated payment""",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    request_enrollment_start_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""From when it is possible to ask for a different enrollment date""",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    request_enrollment_end_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""To when it is possible to ask for a different enrollment date""",
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    program: typing.Optional["AcProgramGQLModel"] = strawberry.field(
        description="""Program associated with this admission""",
        resolver=ScalarResolver['AcProgramGQLModel'](fkey_field_name="program_id"),
        permission_classes=[
            OnlyForAuthentized,
        ],
    )

    payment_info: typing.Optional["PaymentInfoGQLModel"] = strawberry.field(
        description="""Payment information associated with this admission""",
        resolver=ScalarResolver['PaymentInfoGQLModel'](fkey_field_name="payment_info_id"),
        permission_classes=[
            OnlyForAuthentized,
        ]
    )

    exam_types: typing.List["ExamTypeGQLModel"] = strawberry.field(
        description="""Exam types associated with this admission""",
        resolver=VectorResolver["ExamTypeGQLModel"](fkey_field_name="admission_id", whereType=None),
        permission_classes = [
            OnlyForAuthentized,
        ]
    )

    student_admissions: typing.List["StudentAdmissionGQLModel"] = strawberry.field(
        description="""List of student admissions related to the admission""",
        resolver=VectorResolver["StudentAdmissionGQLModel"](fkey_field_name="admission_id", whereType=None),
        permission_classes = [
            OnlyForAuthentized,
        ]
    )


@createInputs
@dataclasses.dataclass
class AdmissionInputFilter:
    id: uuid.UUID
    name: str
    name_en: str
    program_id: str
    application_start_date: datetime.datetime
    application_last_date: datetime.datetime
    end_date: datetime.datetime
    condition_date: datetime.datetime
    request_condition_start_date: datetime.datetime
    request_condition_last_date: datetime.datetime
    request_exam_start_date: datetime.datetime
    request_exam_last_date: datetime.datetime
    payment_date: datetime.datetime
    payment_info_id: uuid.UUID
    request_enrollment_start_date: datetime.datetime
    request_enrollment_last_date: datetime.datetime

admission_by_id = strawberry.field(
    description="""Finds an admission by its id""",
    graphql_type=typing.Optional[AdmissionGQLModel],
    resolver=AdmissionGQLModel.load_with_loader,
    permission_classes=[
        OnlyForAuthentized,
    ]
)

admission_page = strawberry.field(
    description="""Returns a list of admissions""",
    resolver=PageResolver[AdmissionGQLModel](whereType=AdmissionInputFilter),
    permission_classes=[
            OnlyForAuthentized,
    ]
)

########################################################################################################################
#                                                                                                                      #
#                                                    Mutations                                                         #
#                                                                                                                      #
########################################################################################################################

@strawberry.input(description="""Definition of an admission used for creation""")
class AdmissionInsertGQLModel:
    name: str = strawberry.field(description="Name of the admission entry")

    id: typing.Optional[uuid.UUID] = strawberry.field(description="Primary key", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the admission entry", default=None)

    program_id: typing.Optional[uuid.UUID] = strawberry.field(description="Foreign key referencing the associated course", default=None)

    application_start_date: typing.Optional[datetime.datetime] = strawberry.field(description="Od kdy lze podat prihlasku", default=None)
    application_last_date: typing.Optional[datetime.datetime] = strawberry.field(description="Do kdy lze podat prihlasku", default=None)

    end_date: typing.Optional[datetime.datetime] = strawberry.field(description="Admission validity end date",default=None)

    condition_date: typing.Optional[datetime.datetime] = strawberry.field(description="Do kdy dolozit pozadavky",default=None)
    request_condition_start_date: typing.Optional[datetime.datetime] = strawberry.field(description="Od kdy mozne zadat o prodlouzeni", default=None)
    request_condition_last_date: typing.Optional[datetime.datetime] = strawberry.field(description="Do kdz mozne zadat o prodlouzeni", default=None)

    request_exam_start_date: typing.Optional[datetime.datetime] = strawberry.field(description="Od kdy mozne podat zadost o nahradni termin", default=None)
    request_exam_last_date: typing.Optional[datetime.datetime] = strawberry.field(description="Do kdy mozne podat zadost o nahradni termin", default=None)

    payment_date: typing.Optional[datetime.datetime] = strawberry.field(description="Do kdy lze zaplatit poplatek",default=None)
    payment_info_id: typing.Optional[uuid.UUID] = strawberry.field(description="Foreign key referencing the associated payment info", default=None)

    request_enrollment_start_date: typing.Optional[datetime.datetime] = strawberry.field(description="From when it is possible to ask for a different enrollment date", default=None)
    request_enrollment_end_date: typing.Optional[datetime.datetime] = strawberry.field(description="To when it is possible to ask for a different enrollment date", default=None)

    rbacobject_id: typing.Optional[uuid.UUID] = strawberry.field(description="group_id or user_id defines access rights", default=None)
    createdby_id: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="""Definition of an admission used for update""")
class AdmissionUpdateGQLModel:
    id: uuid.UUID = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Last change of the record")

    name: typing.Optional[str] = strawberry.field(description="Name of the admission entry", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the admission entry", default=None)

    program_id: typing.Optional[uuid.UUID] = strawberry.field(description="Foreign key referencing the associated course", default=None)

    application_start_date: typing.Optional[datetime.datetime] = strawberry.field(description="Od kdy lze podat prihlasku", default=None)
    application_last_date: typing.Optional[datetime.datetime] = strawberry.field(description="Do kdy lze podat prihlasku", default=None)

    end_date: typing.Optional[datetime.datetime] = strawberry.field(description="Admission validity end date", default=None)

    condition_date: typing.Optional[datetime.datetime] = strawberry.field(description="Do kdy dolozit pozadavky", default=None)
    request_condition_start_date: typing.Optional[datetime.datetime] = strawberry.field(description="Od kdy mozne zadat o prodlouzeni", default=None)
    request_condition_last_date: typing.Optional[datetime.datetime] = strawberry.field(description="Do kdz mozne zadat o prodlouzeni", default=None)

    request_exam_start_date: typing.Optional[datetime.datetime] = strawberry.field(description="Od kdy mozne podat zadost o nahradni termin", default=None)
    request_exam_last_date: typing.Optional[datetime.datetime] = strawberry.field(description="Do kdy mozne podat zadost o nahradni termin", default=None)

    payment_date: typing.Optional[datetime.datetime] = strawberry.field(description="Do kdy lze zaplatit poplatek", default=None)
    payment_info_id: typing.Optional[uuid.UUID] = strawberry.field(description="Foreign key referencing the associated payment info", default=None)

    request_enrollment_start_date: typing.Optional[datetime.datetime] = strawberry.field(description="From when it is possible to ask for a different enrollment date", default=None)
    request_enrollment_end_date: typing.Optional[datetime.datetime] = strawberry.field(description="To when it is possible to ask for a different enrollment date", default=None)

    changedby_id: strawberry.Private[uuid.UUID] = None


@strawberry.input(description="""Definition of an admission used for delete""")
class AdmissionDeleteGQLModel:
    id: uuid.UUID = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Last change of the record", default=None)

########################################################################################################################

@strawberry.mutation(
    description="Adds an Admission",
    permission_classes=[
        OnlyForAuthentized,
        SimpleInsertPermission[AdmissionGQLModel](roles=["administrátor", "administrátor přijímacího řízení"])
    ]
)
async def admission_insert(self, info: strawberry.types.Info, admission: AdmissionInsertGQLModel) -> typing.Union[AdmissionGQLModel, InsertError[AdmissionGQLModel]]:
    admission.rbacobject_id = admission.rbacobject_id # if admission.rbacobject_id else admission.group_id
    return await Insert[AdmissionInsertGQLModel].DoItSafeWay(info=info, entity=admission)



@strawberry.mutation(
    description="Updates an Admission",
    permission_classes=[
        OnlyForAuthentized,
        SimpleUpdatePermission[AdmissionGQLModel](roles=["administrátor", "administrátor přijímacího řízení"])
    ]
)
async def admission_update(self, info: strawberry.types.Info, admission: typing.Annotated[AdmissionUpdateGQLModel, strawberry.argument(description="desc")]) -> typing.Union[AdmissionGQLModel, UpdateError[AdmissionGQLModel]]:
    return await Update[AdmissionGQLModel].DoItSafeWay(info=info, entity=admission)



@strawberry.mutation(
    description="Deletes an Admission",
    permission_classes=[
        OnlyForAuthentized,
        SimpleDeletePermission[AdmissionGQLModel](roles=["administrátor", "administrátor přijímacího řízení"])
    ]
)
async def admission_delete(self, info: strawberry.types.Info, admission: AdmissionDeleteGQLModel) -> typing.Optional[DeleteError[AdmissionGQLModel]]:
    return await Delete[AdmissionGQLModel].DoItSafeWay(info=info, entity=admission)