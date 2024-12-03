import strawberry
import uuid
import datetime
import typing
import strawberry.types

from uoishelpers.resolvers import getLoadersFromInfo

from .BaseGQLModel import BaseGQLModel

ExamGQLModel = typing.Annotated["ExamGQLModel", strawberry.lazy(".ExamGQLModel")]
StudentAdmissionGQLModel = typing.Annotated["StudentAdmissionGQLModel", strawberry.lazy(".StudentAdmissionGQLModel")]

@strawberry.type(description="Represents an exam result entry associated with an exam and a student admission.")
class ExamResultGQLModel(BaseGQLModel):

    @classmethod
    def get_table_resolvers(cls):
        return {
            "id": lambda row: row.id,
            "score": lambda row: row.score,
            "exam_id": lambda row: row.exam_id,
            "student_admission_id": lambda row: row.student_admission_id,
            "lastchange":lambda row: row.lastchange
        }

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).ExamResultModel

    id: uuid.UUID = strawberry.field()
    score: typing.Optional[float] = strawberry.field(description="Score achieved in the exam result")
    exam_id: uuid.UUID = strawberry.field(description="The ID of the associated exam")
    student_admission_id: uuid.UUID = strawberry.field(description="The ID of the related student admission")
    lastchange: datetime.datetime = strawberry.field(description="Last change of the record")

    @strawberry.field(description="Exam associated with result")
    async def exam(self, info: strawberry.types.Info) -> typing.Optional["ExamGQLModel"]:
        from .ExamGQLModel import ExamGQLModel
        result = await ExamGQLModel.load_with_loader(info=info, id=self.exam_id)
        return result

    @strawberry.field(description="Student admission associated with result")
    async def student_admission(self, info: strawberry.types.Info) -> typing.Optional["StudentAdmissionGQLModel"]:
        from .StudentAdmissionGQLModel import StudentAdmissionGQLModel
        result = await StudentAdmissionGQLModel.load_with_loader(info=info, id=self.student_admission_id)
        return result

@strawberry.field(description="""Returns an exam result by id""")
async def exam_result_by_id(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[ExamResultGQLModel]:
    result = await ExamResultGQLModel.load_with_loader(info=info, id=id)
    return result

@strawberry.field(description="""Returns a list of exam results""")
async def exam_result_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,) -> typing.List[ExamResultGQLModel]:
    loader = getLoadersFromInfo(info).exam_results
    result = await loader.page(skip, limit)
    return result

########################################################################################################################
#                                                                                                                      #
#                                                    Mutations                                                         #
#                                                                                                                      #
########################################################################################################################

@strawberry.input(description="""Definition of an ExamResult used for creation""")
class ExamResultInsertGQLModel:
    id: typing.Optional[uuid.UUID] = strawberry.field(description="primary key", default="")
    score: typing.Optional[float] = strawberry.field(description="Score achieved in the exam result", default=0.0)
    exam_id: uuid.UUID = strawberry.field(description="The ID of the associated exam")
    student_admission_id: uuid.UUID = strawberry.field(description="The ID of the related student admission")

@strawberry.input(description="""Definition of an ExamResult used for creation""")
class ExamResultUpdateGQLModel:
    lastchange: datetime.datetime = strawberry.field(description="Last change of the record")
    id: uuid.UUID = strawberry.field(description="Primary key")

    score: typing.Optional[float] = strawberry.field(description="Score achieved in the exam result", default=None)
    exam_id: uuid.UUID = strawberry.field(description="The ID of the associated exam", default=None)
    student_admission_id: uuid.UUID = strawberry.field(description="The ID of the related student admission", default=None)

@strawberry.input(description="""Definition of an ExamResult used for creation""")
class ExamResultDeleteGQLModel:
    lastchange: datetime.datetime = strawberry.field(description="Last change of the record")
    id: uuid.UUID = strawberry.field(description="Primary key")

@strawberry.type(description="Result of a mutation for an exam result")
class ExamResultMutationResultGQLModel:
    id: uuid.UUID = strawberry.field(description="The ID of the exam result", default=None)
    msg: str = strawberry.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberry.field(description="Returns the exam result")
    async def exam_result(self, info: strawberry.types.Info) -> typing.Union[ExamResultGQLModel, None]:
        result = await ExamResultGQLModel.resolve_reference(info, self.id)
        return result

########################################################################################################################

from uoishelpers.resolvers import Insert, InsertError
@strawberry.mutation(description="Adds a new exam result using stefek magic.")
async def exam_result_insert(self, info: strawberry.types.Info, exam_result: ExamResultInsertGQLModel) -> typing.Union[ExamResultGQLModel, InsertError[ExamResultGQLModel]]:
    result = await Insert[ExamResultGQLModel].DoItSafeWay(info=info, entity=exam_result)
    return result

from uoishelpers.resolvers import Update, UpdateError
@strawberry.mutation(description="Updates an exam result using stefek magic.")
async def exam_result_update(self, info: strawberry.types.Info, exam_result: ExamResultUpdateGQLModel) -> typing.Union[ExamResultGQLModel, UpdateError[ExamResultGQLModel]]:
    result = await Update[ExamResultGQLModel].DoItSafeWay(info=info, entity=exam_result)
    return result

from uoishelpers.resolvers import Delete, DeleteError
@strawberry.mutation(description="Deletes exam result using stefek magic.")
async def exam_result_delete(self, info: strawberry.types.Info, exam_result: ExamResultDeleteGQLModel) -> typing.Optional[DeleteError[ExamResultGQLModel]]:
    result = await Delete[ExamResultGQLModel].DoItSafeWay(info=info, entity=exam_result)
    return result