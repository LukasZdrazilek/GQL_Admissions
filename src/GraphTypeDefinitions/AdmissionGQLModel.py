import strawberry
import uuid
import datetime
import typing

import strawberry.types

from uoishelpers.resolvers import getLoadersFromInfo, getUserFromInfo

from .BaseGQLModel import BaseGQLModel

@strawberry.type(description="""Admission for corresponding year and program""")
class AdmissionGQLModel(BaseGQLModel):

    @classmethod
    def get_table_resolvers(cls):
        return {
            "id": lambda row: row.id,

            "name": lambda row: row.name,
            "name_en": lambda row: row.name_en,

            "state_id": lambda row: row.state_id,
            "program_id": lambda row: row.program_id,

            "application_start_date": lambda row: row.application_start_date,
            "application_last_date": lambda row: row.application_last_date,

            "end_date": lambda row: row.end_date,

            "condition_date": lambda row: row.condition_date,
            "request_condition_start_date": lambda row: row.request_condition_start_date,
            "request_condition_last_date": lambda row: row.request_condition_last_date,

            "request_exam_start_date": lambda row: row.request_exam_start_date,
            "request_exam_last_date": lambda row: row.request_exam_last_date,

            "payment_date": lambda row: row.payment_date,

            "request_enrollment_start_date": lambda row: row.request_enrollment_start_date,
            "request_enrollment_end_date": lambda row: row.request_enrollment_end_date,
        }

    @classmethod
    def getloader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).AdmissionModel

    id: uuid.UUID = strawberry.field()
    name: typing.Optional[str] = strawberry.field(description="Name of the admission entry", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the admission entry", default=None)

    state_id: typing.Optional[uuid.UUID] = strawberry.field(description="stav přijímacího řízení", default=None)
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

@strawberry.field(description="""Returns an admission by id""")
async def admission_by_id(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[AdmissionGQLModel]:
    result = await AdmissionGQLModel.load_with_loader(info=info, id=id)
    return result