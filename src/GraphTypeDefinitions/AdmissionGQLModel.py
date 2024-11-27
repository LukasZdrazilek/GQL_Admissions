import strawberry
import uuid
import datetime
import typing

import strawberry.types
from sqlalchemy.engine import row

from uoishelpers.resolvers import getLoadersFromInfo, getUserFromInfo

from .BaseGQLModel import BaseGQLModel

StudentAdmissionGQLModel = typing.Annotated["StudentAdmissionGQLModel", strawberry.lazy(".StudentAdmissionGQLModel")]
# ExamGQLModel = typing.Annotated["ExamGQLModel", strawberry.lazy(".ExamGQLModel")]
ExamTypeGQLModel = typing.Annotated["ExamTypeGQLModel", strawberry.lazy(".ExamTypeGQLModel")]
# ExamResultGQLModel = typing.Annotated["ExamResultGQLModel", strawberry.lazy(".ExamResultGQLModel")]

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

            "lastchange":lambda row: row.lastchange
        }

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
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

    lastchange: typing.Optional[datetime.datetime] = strawberry.field(description="Last change of the record", default=None)
    
    @strawberry.field(description="Exam types associated with this admission")
    async def exam_types(self, info: strawberry.types.Info) -> typing.List["ExamTypeGQLModel"]:
        from .ExamTypeGQLModel import ExamTypeGQLModel
        loader = ExamTypeGQLModel.getLoader(info=info)
        rows = await loader.filter_by(admission_id=self.id)
        results = [ExamTypeGQLModel.from_sqlalchemy(row) for row in rows]
        return results

    @strawberry.field(description="""List of student admissions related to the admission""")
    async def student_admissions(
            self, info: strawberry.types.Info
    ) -> typing.List["StudentAdmissionGQLModel"]:
        from .StudentAdmissionGQLModel import StudentAdmissionGQLModel
        loader = StudentAdmissionGQLModel.getLoader(info=info)
        rows = await loader.filter_by(admission_id=self.id)
        results = (StudentAdmissionGQLModel.from_sqlalchemy(row) for row in rows)
        return results

@strawberry.field(description="""Returns an admission by id""")
async def admission_by_id(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[AdmissionGQLModel]:
    result = await AdmissionGQLModel.load_with_loader(info=info, id=id)
    return result

@strawberry.field(description="""Returns a list of admissions""")
async def admission_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,) -> typing.List[AdmissionGQLModel]:
    loader = getLoadersFromInfo(info).admissions
    result = await loader.page(skip, limit)
    return result

########################################################################################################################
#                                                                                                                      #
#                                                    Mutations                                                         #
#                                                                                                                      #
########################################################################################################################

@strawberry.input(description="""Definition of an admission used for creation""")
class AdmissionInsertGQLModel:
    id: uuid.UUID = strawberry.field()
    name: typing.Optional[str] = strawberry.field(description="Name of the admission entry", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the admission entry", default=None)

    state_id: typing.Optional[uuid.UUID] = strawberry.field(description="stav přijímacího řízení", default=None)
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

    lastchange: typing.Optional[datetime.datetime] = strawberry.field(description="Last change of the record", default=None)


@strawberry.input(description="""Definition of an admission used for update""")
class AdmissionUpdateGQLModel:
    id: uuid.UUID = strawberry.field()
    name: typing.Optional[str] = strawberry.field(description="Name of the admission entry", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the admission entry", default=None)
    application_start_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="Od kdy lze podat prihlasku", default=None)
    application_last_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="Do kdy lze podat prihlasku", default=None)

    end_date: typing.Optional[datetime.datetime] = strawberry.field(description="Admission validity end date", default=None)

    condition_date: typing.Optional[datetime.datetime] = strawberry.field(description="Do kdy dolozit pozadavky", default=None)
    request_condition_start_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="Od kdy mozne zadat o prodlouzeni", default=None)
    request_condition_last_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="Do kdz mozne zadat o prodlouzeni", default=None)

    request_exam_start_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="Od kdy mozne podat zadost o nahradni termin", default=None)
    request_exam_last_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="Do kdy mozne podat zadost o nahradni termin", default=None)

    payment_date: typing.Optional[datetime.datetime] = strawberry.field(description="Do kdy lze zaplatit poplatek", default=None)

    request_enrollment_start_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="From when it is possible to ask for a different enrollment date", default=None)
    request_enrollment_end_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="To when it is possible to ask for a different enrollment date", default=None)
    
    lastchange: typing.Optional[datetime.datetime] = strawberry.field(description="Last change of the record", default=None)



@strawberry.input(description="""Definition of an admission used for delete""")
class AdmissionDeleteGQLModel:
    id: uuid.UUID = strawberry.field()
    name: typing.Optional[str] = strawberry.field(description="Name of the admission entry", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the admission entry", default=None)
    application_start_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="Od kdy lze podat prihlasku", default=None)
    application_last_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="Do kdy lze podat prihlasku", default=None)

    end_date: typing.Optional[datetime.datetime] = strawberry.field(description="Admission validity end date", default=None)

    condition_date: typing.Optional[datetime.datetime] = strawberry.field(description="Do kdy dolozit pozadavky", default=None)
    request_condition_start_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="Od kdy mozne zadat o prodlouzeni", default=None)
    request_condition_last_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="Do kdz mozne zadat o prodlouzeni", default=None)

    request_exam_start_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="Od kdy mozne podat zadost o nahradni termin", default=None)
    request_exam_last_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="Do kdy mozne podat zadost o nahradni termin", default=None)

    payment_date: typing.Optional[datetime.datetime] = strawberry.field(description="Do kdy lze zaplatit poplatek", default=None)

    request_enrollment_start_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="From when it is possible to ask for a different enrollment date", default=None)
    request_enrollment_end_date: typing.Optional[datetime.datetime] = strawberry.field(
        description="To when it is possible to ask for a different enrollment date", default=None)
    
    lastchange: typing.Optional[datetime.datetime] = strawberry.field(description="Last change of the record", default=None)

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