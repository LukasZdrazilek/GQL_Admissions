import asyncio
import strawberry
import uuid
import datetime
import typing

import strawberry.types

from uoishelpers.resolvers import getLoadersFromInfo, getUserFromInfo

from .BaseGQLModel import BaseGQLModel

AdmissionGQLModel = typing.Annotated["AdmissionGQLModel", strawberry.lazy(".AdmissionGQLModel")]
ExamGQLModel = typing.Annotated["ExamGQLModel", strawberry.lazy(".ExamGQLModel")]
ExamResultGQLModel = typing.Annotated["ExamResultGQLModel", strawberry.lazy(".ExamResultGQLModel")]

@strawberry.type(description="""Student's admission for corresponding admission""")
class StudentAdmissionGQLModel(BaseGQLModel):

    @classmethod
    def get_table_resolvers(cls):
        return {
            "id": lambda row: row.id,

            "admission_id": lambda row: row.admission_id,
            "user_id": lambda row: row.user_id,
            "state_id": lambda row: row.state_id,

            "extended_condition_date": lambda row: row.extended_condition_date,
            "admissioned": lambda row: row.admissioned,
            "enrollment_date": lambda row: row.enrollment_date,
        }

    @classmethod
    def getloader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).StudentAdmissionModel

    id: uuid.UUID = strawberry.field()
    admission_id: uuid.UUID = strawberry.field(description="UUID of an admission")
    user_id: typing.Optional[uuid.UUID] = strawberry.field(description="UUID of a user")
    state_id: typing.Optional[uuid.UUID] = strawberry.field(description="UUID of a state")
    extended_condition_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of extended condition")
    admissioned: typing.Optional[bool] = strawberry.field(description="True if an admissioned admission")
    enrollment_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of enrollment")

    @strawberry.field(description="The admission to which Student Admission belong")
    async def admission(self, info: strawberry.types.Info) -> typing.Optional["AdmissionGQLModel"]:
        from .AdmissionGQLModel import AdmissionGQLModel
        result = await AdmissionGQLModel.load_with_loader(info=info, id=self.admission_id)
        return result

    @strawberry.field(description="Exam results related to the student admission")
    async def exam_results(
            self, info: strawberry.types.Info
    ) -> typing.Optional[typing.List["ExamResultGQLModel"]]:
        from .ExamResultGQLModel import ExamResultGQLModel
        loader = ExamResultGQLModel.getloader(info=info)
        rows = await loader.filter_by(student_admission_id=self.id)
        results = (ExamResultGQLModel.from_sqlalchemy(row) for row in rows)
        return results

    @strawberry.field(description="Exams related to the student admission")
    async def exams(self, info: strawberry.types.Info) -> typing.Optional[typing.List["ExamGQLModel"]]:
        from .ExamGQLModel import ExamGQLModel
        loader = getLoadersFromInfo(info).student_exam_links
        rows = await loader.filter_by(student_id=self.id)
        awaitable = (ExamGQLModel.resolve_reference(info, row.exam_id) for row in rows)
        return await asyncio.gather(*awaitable)

@strawberry.field(description="""Returns a Student Admission by id""")
async def studentadmission_by_id(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[StudentAdmissionGQLModel]:
    result = await StudentAdmissionGQLModel.load_with_loader(info=info, id=id)
    return result

@strawberry.field(description="""Returns a list of student admissions""")
async def studentadmission_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,) -> typing.List[StudentAdmissionGQLModel]:
    loader = getLoadersFromInfo(info).student_admissions
    result = await loader.page(skip, limit)
    return result

########################################################################################################################
#                                                                                                                      #
#                                                    Mutations                                                         #
#                                                                                                                      #
########################################################################################################################

@strawberry.input(description="""Definition of an student admission used for creation""")
class StudentAdmissionInsertGQLModel:
    id: typing.Optional[uuid.UUID] = strawberry.field()
    admission_id: uuid.UUID = strawberry.field(description="UUID of an admission")
    user_id: typing.Optional[uuid.UUID] = strawberry.field(description="UUID of a user")
    state_id: typing.Optional[uuid.UUID] = strawberry.field(description="UUID of a state")
    extended_condition_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of extended condition")
    admissioned: typing.Optional[bool] = strawberry.field(description="True if an admissioned admission")
    enrollment_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of enrollment")

@strawberry.type(description="Result of a mutation for a student admission")
class StudentAdmissionResultGQLModel:
    id: uuid.UUID = strawberry.field(description="The ID of the student admission", default=None)
    msg: str = strawberry.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberry.field(description="Returns the student admission")
    async def student_admission(self, info: strawberry.types.Info) -> typing.Union[StudentAdmissionGQLModel, None]:
        result = await StudentAdmissionGQLModel.resolve_reference(info, self.id)
        return result

@strawberry.mutation(description="Adds a new admission.")
async def student_admission_insert(self, info: strawberry.types.Info, student_admission: StudentAdmissionInsertGQLModel) -> StudentAdmissionResultGQLModel:
    loader = getLoadersFromInfo(info).student_admissions
    row = await loader.insert(student_admission)
    result = StudentAdmissionResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result