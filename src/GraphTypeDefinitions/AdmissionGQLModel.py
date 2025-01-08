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
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="""English name of the admission entry""",
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    program_id: typing.Optional[uuid.UUID] = strawberry.field(
        default=None,
        description="""Foreign key referencing to the associated program""",
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    application_start_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Od kdy lze podat přihlášku""",
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    application_last_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Do kdy lze podat přihlášku""",
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    end_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Admission validity end date""",
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    condition_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Do kdy doložit požadavky""",
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    request_condition_start_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Od kdy možné žádat o prodloužení""",
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    request_condition_last_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Do kdy možné žádat o prodloužení""",
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    request_exam_start_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Od kdy možné podat žádost o náhradní termín""",
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    request_exam_last_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Do kdy možné podat žádost o náhradní termín""",
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    payment_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""Do kdy lze zaplatit poplatek""",
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    request_enrollment_start_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""From when it is possible to ask for a different enrollment date""",
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    request_enrollment_end_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="""To when it is possible to ask for a different enrollment date""",
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    program: typing.Optional["AcProgramGQLModel"] = strawberry.field(
        description="""Program associated with this admission""",
        resolver=ScalarResolver['ExamTypeGQLModel'](fkey_field_name="program_id"),
        # permission_classes=[
        #     OnlyForAuthenticated
        # ],
    )

    exam_types: typing.List["ExamTypeGQLModel"] = strawberry.field(
        description="""Exam types associated with this admission""",
        resolver=VectorResolver["ExamTypeGQLModel"](fkey_field_name="admission_id", whereType=None),
        # permission_classes = [
        #     OnlyForAuthentized,
        # ]
    )

    student_admissions: typing.List["StudentAdmissionGQLModel"] = strawberry.field(
        description="""List of student admissions related to the admission""",
        resolver=VectorResolver["StudentAdmissionGQLModel"](fkey_field_name="admission_id", whereType=None),
        # permission_classes = [
        #     OnlyForAuthentized,
        # ]
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
    request_enrollment_start_date: datetime.datetime
    request_enrollment_last_date: datetime.datetime

admission_by_id = strawberry.field(
    description="""Finds an admission by its id""",
    graphql_type=typing.Optional[AdmissionGQLModel],
    resolver=AdmissionGQLModel.load_with_loader,
    # permission_classes=[
    #     OnlyForAuthentized,
    # ]
        )

admission_page = strawberry.field(
    description="""Returns a list of admissions""",
    resolver=PageResolver[AdmissionGQLModel](whereType=AdmissionInputFilter),
    # permission_classes=[
    #         OnlyForAuthentized,
    # ]
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

    request_enrollment_start_date: typing.Optional[datetime.datetime] = strawberry.field(description="From when it is possible to ask for a different enrollment date", default=None)
    request_enrollment_end_date: typing.Optional[datetime.datetime] = strawberry.field(description="To when it is possible to ask for a different enrollment date", default=None)

    changedby_id: strawberry.Private[uuid.UUID] = None


@strawberry.input(description="""Definition of an admission used for delete""")
class AdmissionDeleteGQLModel:
    id: uuid.UUID = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Last change of the record", default=None)

########################################################################################################################

@strawberry.type(description="Result of a mutation for an admission")
class AdmissionMutationResultGQLModel:
    id: uuid.UUID = strawberry.field(description="The ID of the admission", default=None)
    msg: str = strawberry.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberry.field(description="Returns the admission")
    async def admission(self, info: strawberry.types.Info) -> typing.Union[AdmissionGQLModel, None]:
        result = await AdmissionGQLModel.resolve_reference(info, self.id)
        return result

from uoishelpers.resolvers import Insert, InsertError
@strawberry.mutation(description="Adds a new admission using stefek magic.")
async def admission_insert(self, info: strawberry.types.Info, admission: AdmissionInsertGQLModel) -> typing.Union[AdmissionGQLModel, InsertError[AdmissionGQLModel]]:
    result = await Insert[AdmissionGQLModel].DoItSafeWay(info=info, entity=admission)
    return result

from uoishelpers.resolvers import Update, UpdateError
@strawberry.mutation(description="Updates an admission using stefek magic.")
async def admission_update(self, info: strawberry.types.Info, admission: AdmissionUpdateGQLModel) -> typing.Union[AdmissionGQLModel, UpdateError[AdmissionGQLModel]]:
    result = await Update[AdmissionGQLModel].DoItSafeWay(info=info, entity=admission)
    return result

from uoishelpers.resolvers import Delete, DeleteError
@strawberry.mutation(description="Deletes admission using stefek magic.")
async def admission_delete(self, info: strawberry.types.Info, admission: AdmissionDeleteGQLModel) -> typing.Union[AdmissionGQLModel, DeleteError[AdmissionGQLModel]]:
    result = await Delete[AdmissionGQLModel].DoItSafeWay(info=info, entity=admission)
    return result