import strawberry
import uuid
import datetime
import typing

import strawberry.types

from uoishelpers.resolvers import getLoadersFromInfo

from .BaseGQLModel import BaseGQLModel

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
            "date": lambda row: row.date,
            "exam_type_id": lambda row: row.exam_type_id,
        }
    
    @classmethod
    def getloader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).ExamModel

    id: uuid.UUID = strawberry.field()
    name: str = strawberry.field(description="Name of the exam type")
    name_en: str = strawberry.field(description="English name of the exam type")
    date: datetime.datetime = strawberry.field(description="Date of the exam")
    exam_type_id: uuid.UUID = strawberry.field(description="Foreign key to exam type")

    @strawberry.field(description="Type of the exam")
    async def exam_type(self, info: strawberry.types.Info) -> typing.Optional["ExamTypeGQLModel"]:
        from .ExamTypeGQLModel import ExamTypeGQLModel
        result = await ExamTypeGQLModel.load_with_loader(info=info, id=self.exam_type_id)
        return result

    @strawberry.field(description="Results of the exam")
    async def exam_results(self, info: strawberry.types.Info) -> typing.List["ExamResultGQLModel"]:
        from .ExamResultGQLModel import ExamResultGQLModel
        loader = ExamResultGQLModel.getloader(info=info)
        rows = await loader.filter_by(exam_id=self.id)
        results = (ExamResultGQLModel.from_sqlalchemy(row) for row in rows)
        return results
