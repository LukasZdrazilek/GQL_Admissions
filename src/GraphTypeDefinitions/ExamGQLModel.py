import asyncio

import strawberry
import uuid
import datetime
import typing

import strawberry.types

from uoishelpers.resolvers import getLoadersFromInfo

from .BaseGQLModel import BaseGQLModel

StudentAdmissionGQLModel = typing.Annotated["StudentAdmissionGQLModel", strawberry.lazy(".StudentAdmissionGQLModel")]
ExamResultGQLModel = typing.Annotated["ExamResultGQLModel", strawberry.lazy(".ExamResultGQLModel")]
ExamTypeGQLModel = typing.Annotated["ExamTypeGQLModel", strawberry.lazy(".ExamTypeGQLModel")]

@strawberry.type(description="Represents an actual exam on a certain date")
class ExamGQLModel(BaseGQLModel):

    @classmethod
    def get_table_resolvers(cls):
        return {
            "id": lambda row: row.id, 
            "name": lambda row: row.name,
            "name_en": lambda row: row.name_en,
            "exam_date": lambda row: row.exam_date,
            "exam_type_id": lambda row: row.exam_type_id,

            "lastchange": lambda row: row.lastchange,
            "created": lambda row: row.created,
            "createdby_id": lambda row: row.createdby_id,
            "changedby_id": lambda row: row.changedby_id,
            "rbaobject_id": lambda row: row.rbaobject_id,
            "valid": lambda row: row.valid,
        }
    
    @classmethod
    def getloader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).ExamModel

    id: uuid.UUID = strawberry.field()
    name: typing.Optional[str] = strawberry.field(description="Name of the exam type")
    name_en: typing.Optional[str] = strawberry.field(description="English name of the exam type")
    exam_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of the exam")
    exam_type_id: uuid.UUID = strawberry.field(description="Foreign key to exam type")

    @strawberry.field(description="Type of the exam")
    async def exam_type(self, info: strawberry.types.Info) -> typing.Optional["ExamTypeGQLModel"]:
        from .ExamTypeGQLModel import ExamTypeGQLModel
        result = await ExamTypeGQLModel.load_with_loader(info=info, id=self.exam_type_id)
        return result

    @strawberry.field(description="Results of the exam")
    async def exam_results(
            self, info: strawberry.types.Info
    ) -> typing.List["ExamResultGQLModel"]:
        from .ExamResultGQLModel import ExamResultGQLModel
        loader = ExamResultGQLModel.getloader(info=info)
        rows = await loader.filter_by(exam_id=self.id)
        results = (ExamResultGQLModel.from_sqlalchemy(row) for row in rows)
        return results

    @strawberry.field(description="Student's Exams")
    async def students(self, info: strawberry.types.Info) -> typing.List["StudentAdmissionGQLModel"]:
        from .StudentAdmissionGQLModel import StudentAdmissionGQLModel
        loader = getLoadersFromInfo(info).student_exam_links
        rows = await loader.filter_by(exam_id=self.id)
        awaitable = (StudentAdmissionGQLModel.resolve_reference(info, row.student_id) for row in rows)
        return await asyncio.gather(*awaitable)

@strawberry.field(description="""Returns an Exam by id""")
async def exam_by_id(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[ExamGQLModel]:
    result = await ExamGQLModel.load_with_loader(info=info, id=id)
    return result

@strawberry.field(description="""Returns a list of exams""")
async def exam_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,) -> typing.List[ExamGQLModel]:
    loader = getLoadersFromInfo(info).exams
    result = await loader.page(skip, limit)
    return result

########################################################################################################################
#                                                                                                                      #
#                                                    Mutations                                                         #
#                                                                                                                      #
########################################################################################################################

@strawberry.input(description="Definition of an exam used for creation")
class ExamInsertGQLModel:
    id: uuid.UUID = strawberry.field(description="The ID of the exam")
    name: typing.Optional[str] = strawberry.field(description="Name of the exam type", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the exam type", default=None)
    exam_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of the exam", default=None)
    exam_type_id: uuid.UUID = strawberry.field(description="Foreign key to exam type")

@strawberry.mutation(description="Adds a new exam.")
async def exam_insert(self, info: strawberry.types.Info, exam: ExamInsertGQLModel) -> ExamGQLModel:
    loader = getLoadersFromInfo(info).exams
    row = await loader.insert(exam)
    result = ExamGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result