import strawberry
import uuid
import typing
import strawberry.types

from uoishelpers.resolvers import getLoadersFromInfo

from .BaseGQLModel import BaseGQLModel
ExamGQLModel = typing.Annotated["ExamGQLModel", strawberry.lazy(".ExamGQLModel")]
#StudentAdmissionGQLModel = typing.Annotated["StudentAdmissionGQLModel", strawberry.lazy(".StudentAdmissionGQLModel")]

@strawberry.type(description="Represents an exam result entry associated with an exam and a student admission.")
class ExamResultGQLModel(BaseGQLModel):

    @classmethod
    def get_table_resolvers(cls):
        return {
            "id": lambda row: row.id,
            "score": lambda row: row.score,
            "exam_id": lambda row: row.exam_id,
            "student_admission_id": lambda row: row.student_admission_id,
        }

    @classmethod
    def getloader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).ExamResultModel

    id: uuid.UUID = strawberry.field()
    score: float = strawberry.field(description="Score achieved in the exam result")
    
    exam_id: uuid.UUID = strawberry.field(description="The ID of the associated exam")
    student_admission_id: uuid.UUID = strawberry.field(description="The ID of the related student admission")

    @strawberry.field(description="The exam associated with this result")
    async def exam(self, info: strawberry.types.Info) -> typing.Optional[ExamGQLModel]:
        loader = ExamGQLModel.getloader(info=info)
        return await loader.load(self.exam_id)

    # @strawberry.field(description="The student admission associated with this result")
    # async def student_admission(self, info: strawberry.types.Info) -> typing.Optional[StudentAdmissionGQLModel]:
    #     loader = StudentAdmissionGQLModel.getloader(info=info)
    #     return await loader.load(self.student_admission_id)
