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
            "lastchange":lambda row: row.lastchange
        }
    
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).ExamModel

    id: uuid.UUID = strawberry.field()
    name: typing.Optional[str] = strawberry.field(description="Name of the exam type")
    name_en: typing.Optional[str] = strawberry.field(description="English name of the exam type")
    exam_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of the exam")
    exam_type_id: uuid.UUID = strawberry.field(description="Foreign key to exam type")
    lastchange: datetime.datetime = strawberry.field(description="Last change of the record")

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
        loader = ExamResultGQLModel.getLoader(info=info)
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
    name: str = strawberry.field(description="Name of the exam type")
    id: typing.Optional[uuid.UUID] = strawberry.field(description="The ID of the exam", default="")
    exam_type_id: typing.Optional[uuid.UUID] = strawberry.field(description="Foreign key to exam type", default="")

    name_en: typing.Optional[str] = strawberry.field(description="English name of the exam type", default="")
    exam_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of the exam", default="")

@strawberry.input(description="Definition of an exam used for creation")
class ExamUpdateGQLModel:
    lastchange: datetime.datetime = strawberry.field(description="Last change of the record")
    id: uuid.UUID = strawberry.field(description="The ID of the exam")
    
    name: typing.Optional[str] = strawberry.field(description="Name of the exam type", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the exam type", default=None)
    exam_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of the exam", default=None)
    exam_type_id: uuid.UUID = strawberry.field(description="Foreign key to exam type", default=None)

@strawberry.input(description="Definition of an exam used for creation")
class ExamDeleteGQLModel:
    lastchange: datetime.datetime = strawberry.field(description="Last change of the record")
    id: uuid.UUID = strawberry.field(description="The ID of the exam")

@strawberry.type(description="Result of a mutation for an exam")
class ExamMutationResultGQLModel:
    id: uuid.UUID = strawberry.field(description="The ID of the exam", default=None)
    msg: str = strawberry.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberry.field(description="Returns the exam type")
    async def exam(self, info: strawberry.types.Info) -> typing.Union[ExamGQLModel, None]:
        result = await ExamGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.input(description="Definition of an StudentExam Link used for addition")
class StudentExamLinkAddGQLModel:
    exam_id: typing.Optional[uuid.UUID] = strawberry.field(description="The ID of the exam")
    student_id: typing.Optional[uuid.UUID] = strawberry.field(description="The ID of the student")

########################################################################################################################

@strawberry.mutation(description="Adds a new StudentExam link.")
async def student_exam_link_add(self, info: strawberry.types.Info, link: StudentExamLinkAddGQLModel) -> ExamMutationResultGQLModel:
    loader = getLoadersFromInfo(info).student_exam_links
    rows = await loader.filter_by(exam_id=link.exam_id, student_id=link.student_id)
    row = next(rows, None)
    result = ExamMutationResultGQLModel()
    if row is None:
        row = await loader.insert(link)
        result.msg = "ok"
    if row is not None:
        result.msg = "exists"
    result.id = link.exam_id
    return result

from uoishelpers.resolvers import Insert, InsertError
@strawberry.mutation(description="Adds a new exam using stefek magic.")
async def exam_insert(self, info: strawberry.types.Info, exam: ExamInsertGQLModel) -> typing.Union[ExamGQLModel, InsertError[ExamGQLModel]]:
    result = await Insert[ExamGQLModel].DoItSafeWay(info=info, entity=exam)
    return result

from uoishelpers.resolvers import Update, UpdateError
@strawberry.mutation(description="Updates an exam using stefek magic.")
async def exam_update(self, info: strawberry.types.Info, exam: ExamUpdateGQLModel) -> typing.Union[ExamGQLModel, UpdateError[ExamGQLModel]]:
    result = await Update[ExamGQLModel].DoItSafeWay(info=info, entity=exam)
    return result

from uoishelpers.resolvers import Delete, DeleteError
@strawberry.mutation(description="Deletes exam using stefek magic.")
async def exam_delete(self, info: strawberry.types.Info, exam: ExamDeleteGQLModel) -> typing.Optional[DeleteError[ExamGQLModel]]:
    result = await Delete[ExamGQLModel].DoItSafeWay(info=info, entity=exam)
    return result