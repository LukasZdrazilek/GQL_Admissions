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
    VectorResolver,
    ScalarResolver,
)


from .BaseGQLModel import BaseGQLModel

StudentAdmissionGQLModel = typing.Annotated["StudentAdmissionGQLModel", strawberry.lazy(".StudentAdmissionGQLModel")]
ExamResultGQLModel = typing.Annotated["ExamResultGQLModel", strawberry.lazy(".ExamResultGQLModel")]
ExamTypeGQLModel = typing.Annotated["ExamTypeGQLModel", strawberry.lazy(".ExamTypeGQLModel")]
FacilityGQLModel = typing.Annotated["FacilityGQLModel", strawberry.lazy(".FacilityGQLModel")]
GroupGQLModel = typing.Annotated["GroupGQLModel", strawberry.lazy(".GroupGQLModel")]


@strawberry.federation.type(
    keys=["id"], description="""Represents an actual exam on a certain date"""
)
class ExamGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).ExamModel

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="Name of the exam type"
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    name_en: typing.Optional[str] = strawberry.field(
        default=None,
        description="English name of the exam type"
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    exam_date: typing.Optional[datetime.datetime] = strawberry.field(
        default=None,
        description="Date of the exam"
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    examiners_id: typing.Optional[uuid.UUID] = strawberry.field(
        default=None,
        description="Foreign key referencing to group of examiners",
        # permission_classes=[
        #     OnlyForAuthentized,
        # ]
    )

    facility_id: typing.Optional[uuid.UUID] = strawberry.field(
        default=None,
        description="Foreign key referencing to facility of exam",
        # permission_classes=[
        #     OnlyForAuthentized,
        # ]
    )

    exam_type_id: uuid.UUID = strawberry.field(
        description="Foreign key to exam type"
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )

    facility: typing.Optional["FacilityGQLModel"] = strawberry.field(
        description="""Facility associated with this exam""",
        resolver=ScalarResolver['FacilityGQLModel'](fkey_field_name="facility_id"),
        # permission_classes=[
        #     OnlyForAuthenticated
        # ],
    )

    examiners: typing.Optional["GroupGQLModel"] = strawberry.field(
        description="""Examiners associated with this exam""",
        resolver=ScalarResolver['GroupGQLModel'](fkey_field_name="examiners_id"),
        # permission_classes=[
        #     OnlyForAuthenticated
        # ],
    )

    exam_type: typing.Optional["ExamTypeGQLModel"] = strawberry.field(
        description="""Type of the exam""",
        resolver=ScalarResolver['ExamTypeGQLModel'](fkey_field_name="exam_type_id"),
        # permission_classes=[
        #     OnlyForAuthenticated
        # ],
    )

    exam_results: typing.List["ExamResultGQLModel"] = strawberry.field(
        description="""Results of the exam""",
        resolver=VectorResolver["ExamResultGQLModel"](fkey_field_name="exam_id", whereType=None),
        # permission_classes = [
        #     OnlyForAuthorized,
        # ]
    )

    @strawberry.field(
        description="Student Admissions related to this exam",
        # permission_classes=[
        #   OnlyForAuthenticated
        # ]
    )
    async def student_admission(self, info: strawberry.types.Info) -> typing.List["StudentAdmissionGQLModel"]:
        from .StudentAdmissionGQLModel import StudentAdmissionGQLModel
        loader = getLoadersFromInfo(info).student_exam_links
        rows = await loader.filter_by(exam_id=self.id)
        awaitable = (StudentAdmissionGQLModel.resolve_reference(info, row.student_id) for row in rows)
        return await asyncio.gather(*awaitable)

@createInputs
@dataclasses.dataclass
class ExamInputFilter:
    id: uuid.UUID
    name: str
    name_en: str

exam_by_id = strawberry.field(
    description = """Finds an Exam by its id""",
    graphql_type=typing.Optional[ExamGQLModel],
    resolver=ExamGQLModel.load_with_loader,
    # permission_classes=[
    #     OnlyForAuthentized,
    # ]
)

exam_page = strawberry.field(
    description="""Returns a list of exams""",
    # permission_classes=[OnlyForAuthentized],
    resolver=PageResolver[ExamGQLModel](whereType=ExamInputFilter)  # Use appropriate filter if needed
)


########################################################################################################################
#                                                                                                                      #
#                                                    Mutations                                                         #
#                                                                                                                      #
########################################################################################################################

@strawberry.input(description="Definition of an exam used for creation")
class ExamInsertGQLModel:
    name: str = strawberry.field(description="Name of the exam type")
    exam_type_id: uuid.UUID = strawberry.field(description="Foreign key to exam type")

    id: typing.Optional[uuid.UUID] = strawberry.field(description="Primary key", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the exam type", default=None)
    exam_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of the exam", default=None)
    examiners_id: typing.Optional[uuid.UUID] = strawberry.field(description="Foreign key to group of examiners", default=None)
    facility_id: typing.Optional[uuid.UUID] = strawberry.field(description="Foreign key referencing to facility", default=None)

    rbacobject_id: typing.Optional[uuid.UUID] = strawberry.field(description="group_id or user_id defines access rights", default=None)
    createdby_id: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="Definition of an exam used for creation")
class ExamUpdateGQLModel:
    id: uuid.UUID = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Last change of the record")

    name: typing.Optional[str] = strawberry.field(description="Name of the exam type", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the exam type", default=None)
    exam_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of the exam", default=None)
    examiners_id: typing.Optional[uuid.UUID] = strawberry.field(description="Foreign key to group of examiners", default=None)
    facility_id: typing.Optional[uuid.UUID] = strawberry.field(description="Foreign key referencing to facility",default=None)
    exam_type_id: typing.Optional[uuid.UUID] = strawberry.field(description="Foreign key to exam type", default=None)

    changedby_id: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="Definition of an exam used for creation")
class ExamDeleteGQLModel:
    id: uuid.UUID = strawberry.field(description="Primary key")
    lastchange: datetime.datetime = strawberry.field(description="Last change of the record")

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

from uoishelpers.resolvers import InsertError
@strawberry.mutation(description="""Links student to exam""")
async def link_student_to_exam(self, info: strawberry.types.Info, link: StudentExamLinkAddGQLModel) -> typing.Union[ExamGQLModel, InsertError[ExamGQLModel]]:#ExamMutationResultGQLModel:
    loader = getLoadersFromInfo(info).student_exam_links
    rows = await loader.filter_by(exam_id=link.exam_id, student_id=link.student_id)
    row = next(rows, None)
    if row is None:
        row = await loader.insert(link)
        result = await ExamGQLModel.resolve_reference(info, link.exam_id)
        return result

    result = InsertError[ExamGQLModel]()
    result.msg = "item exists"
    result.input = link
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
async def exam_delete(self, info: strawberry.types.Info, exam: ExamDeleteGQLModel) -> typing.Union[ExamGQLModel, DeleteError[ExamGQLModel]]:
    result = await Delete[ExamGQLModel].DoItSafeWay(info=info, entity=exam)
    return result