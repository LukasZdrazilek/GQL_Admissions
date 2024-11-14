import strawberry
import uuid
import datetime
import typing

import strawberry.types

from uoishelpers.resolvers import getLoadersFromInfo, getUserFromInfo

from .BaseGQLModel import BaseGQLModel

AdmissionGQLModel = typing.Annotated["AdmissionGQLModel", strawberry.lazy(".AdmissionGQLModel")]

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
    admission_id: typing.Optional[uuid.UUID] = strawberry.field(description="UUID of an admission")
    user_id: typing.Optional[uuid.UUID] = strawberry.field(description="UUID of a user")
    state_id: typing.Optional[uuid.UUID] = strawberry.field(description="UUID of a state")
    extended_condition_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of extended condition")
    admissioned: typing.Optional[bool] = strawberry.field(description="True if an admissioned admission")
    enrollment_date: typing.Optional[datetime.datetime] = strawberry.field(description="Date of enrollment")

    @strawberry.field(description="")
    async def admission(self, info: strawberry.types.Info) -> typing.Optional["AdmissionGQLModel"]:
        from .AdmissionGQLModel import AdmissionGQLModel
        result = await AdmissionGQLModel.load_with_loader(info=info, id=self.admission_id)
        return result

@strawberry.field(description="""Returns a Student Admission by id""")
async def studentadmission_by_id(self, info: strawberry.types.Info, id: uuid.UUID) -> typing.Optional[StudentAdmissionGQLModel]:
    result = await StudentAdmissionGQLModel.load_with_loader(info=info, id=id)
    return result