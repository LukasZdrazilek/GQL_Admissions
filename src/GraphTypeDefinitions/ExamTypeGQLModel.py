import strawberry
import uuid
import typing
import datetime
from uoishelpers.resolvers import getLoadersFromInfo
from .BaseGQLModel import BaseGQLModel

AdmissionGQLModel = typing.Annotated["AdmissionGQLModel", strawberry.lazy(".AdmissionGQLModel")]
ExamGQLModel = typing.Annotated["ExamGQLModel", strawberry.lazy(".ExamGQLModel")]

@strawberry.type(description="Represents a type of exam associated with an admission, including metadata.")
class ExamTypeGQLModel(BaseGQLModel):

    @classmethod
    def get_table_resolvers(cls):
        return {
            "id": lambda row: row.id,
            "name": lambda row: row.name,
            "name_en": lambda row: row.name_en,
            "min_score": lambda row: row.min_score,
            "max_score": lambda row: row.max_score,
            "admission_id": lambda row: row.admission_id,
        }

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).ExamTypeModel

    id: uuid.UUID = strawberry.field()
    name: typing.Optional[str] = strawberry.field(description="Name of the exam type", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the exam type", default=None)
    min_score: typing.Optional[float] = strawberry.field(description="Minimum score for this exam type", default=None)
    max_score: typing.Optional[float] = strawberry.field(description="Maximum score for this exam type", default=None)
    admission_id: uuid.UUID = strawberry.field(description="The ID of the associated admission")

    @strawberry.field(description="The admission to which ExamType belong")
    async def admission(self, info: strawberry.types.Info) -> typing.Optional["AdmissionGQLModel"]:
        from .AdmissionGQLModel import AdmissionGQLModel
        result = await AdmissionGQLModel.load_with_loader(info=info, id=self.admission_id)
        return result

    @strawberry.field(description="Exams of corresponding exam type")
    async def exams(
            self, info: strawberry.types.Info
    ) -> typing.List["ExamGQLModel"]:
        from .ExamGQLModel import ExamGQLModel
        loader = ExamGQLModel.getloader(info=info)
        rows = await loader.filter_by(exam_type_id=self.id)
        results = (ExamGQLModel.from_sqlalchemy(row) for row in rows)
        return results

@strawberry.field(description="""Returns a Student Admission by id""")
async def exam_type_by_id(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[ExamTypeGQLModel]:
    result = await ExamTypeGQLModel.load_with_loader(info=info, id=id)
    return result

@strawberry.field(description="""Returns a list of exam types""")
async def exam_type_page(self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,) -> typing.List[ExamTypeGQLModel]:
    loader = getLoadersFromInfo(info).exam_types
    result = await loader.page(skip, limit)
    return result

########################################################################################################################
#                                                                                                                      #
#                                                    Mutations                                                         #
#                                                                                                                      #
########################################################################################################################

@strawberry.input(description="""Definition of an exam type used for creation""")
class ExamTypeInsertGQLModel:
    id: uuid.UUID = strawberry.field()
    name: typing.Optional[str] = strawberry.field(description="Name of the exam type", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the exam type", default=None)
    min_score: typing.Optional[float] = strawberry.field(description="Minimum score for this exam type", default=None)
    max_score: typing.Optional[float] = strawberry.field(description="Maximum score for this exam type", default=None)
    admission_id: uuid.UUID = strawberry.field(description="The ID of the associated admission")

@strawberry.type(description="Result of a mutation for an exam type")
class ExamTypeMutationResultGQLModel:
    id: uuid.UUID = strawberry.field(description="The ID of the exam type", default=None)
    msg: str = strawberry.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberry.field(description="Returns the exam type")
    async def exam_type(self, info: strawberry.types.Info) -> typing.Union[ExamTypeGQLModel, None]:
        result = await ExamTypeGQLModel.resolve_reference(info, self.id)
        return result

# @strawberry.mutation(description="Adds a new exam type.")
# async def exam_type_insert(self, info: strawberry.types.Info,
#                            exam_type: ExamTypeInsertGQLModel) -> ExamTypeMutationResultGQLModel:
#     loader = getLoadersFromInfo(info).exam_types
#     row = await loader.insert(exam_type)
#     result = ExamTypeMutationResultGQLModel()
#     result.msg = "ok"
#     result.id = row.id
#     return result

from uoishelpers.resolvers import Insert, InsertError
@strawberry.mutation(description="Adds a new exam type using stefek magic.")
async def exam_type_insert(self, info: strawberry.types.Info, exam_type: ExamTypeInsertGQLModel) -> typing.Union[ExamTypeGQLModel, InsertError[ExamTypeGQLModel]]:
    result = await Insert[ExamTypeGQLModel].DoItSafeWay(info=info, entity=exam_type)
    return result