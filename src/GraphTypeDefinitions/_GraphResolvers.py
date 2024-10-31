import strawberry
import uuid
import datetime
import typing
from src.GraphPermissions import OnlyForAuthentized

UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".externals")]
AdmissionGQLModel = typing.Annotated["AdmissionGQLModel", strawberry.lazy(".admissions")]
ExamTypeGQLModel = typing.Annotated["ExamTypeGQLModel", strawberry.lazy(".exams")]
DisciplineTypeGQLModel = typing.Annotated["DisciplineTypeGQLModel", strawberry.lazy(".disciplines")]

@strawberry.field(description="Entity primary key", permission_classes=[OnlyForAuthentized()])
def resolve_id(self) -> uuid.UUID:
    return self.id

@strawberry.field(description="Entity name", permission_classes=[OnlyForAuthentized()])
def resolve_name(self) -> str:
    return self.name

@strawberry.field(description="Entity english name", permission_classes=[OnlyForAuthentized()])
def resolve_name_en(self) -> str:
    return self.name_en if self.name_en else ""

@strawberry.field(description="Entity start date")
def resolve_startdate(self) -> datetime.date:
    return self.startdate

@strawberry.field(description="Entity end date")
def resolve_enddate(self) -> datetime.date:
    return self.enddate

@strawberry.field(description="Validity of event", permission_classes=[OnlyForAuthentized()])
def resolve_valid(self) -> bool:
    return self.valid

@strawberry.field(description="Creation time", permission_classes=[OnlyForAuthentized()])
def resolve_created(self) -> typing.Optional[datetime.datetime]:
    return self.created

@strawberry.field(description="Timestamp of last change", permission_classes=[OnlyForAuthentized()])
def resolve_lastchange(self) -> typing.Optional[datetime.datetime]:
    return self.lastchange

@strawberry.field(description="User who created the entity", permission_classes=[OnlyForAuthentized()])
async def resolve_createdby(self, info) -> typing.Optional[UserGQLModel]:
    return await resolve_user(info, self.createdby)

@strawberry.field(description="User who last changed the entity", permission_classes=[OnlyForAuthentized()])
async def resolve_changedby(self, info) -> typing.Optional[UserGQLModel]:
    return await resolve_user(info, self.changedby)

@strawberry.field(description="Related admission entity", permission_classes=[OnlyForAuthentized()])
async def resolve_admission(self, info) -> typing.Optional[AdmissionGQLModel]:
    from .admissions import AdmissionGQLModel
    return await AdmissionGQLModel.resolve_reference(info, self.admission_id)

@strawberry.field(description="Related exam type", permission_classes=[OnlyForAuthentized()])
async def resolve_examtype(self, info) -> typing.Optional[ExamTypeGQLModel]:
    from .exams import ExamTypeGQLModel
    return await ExamTypeGQLModel.resolve_reference(info, self.examtype_id)

@strawberry.field(description="Related discipline type", permission_classes=[OnlyForAuthentized()])
async def resolve_disciplinetype(self, info) -> typing.Optional[DisciplineTypeGQLModel]:
    from .disciplines import DisciplineTypeGQLModel
    return await DisciplineTypeGQLModel.resolve_reference(info, self.disciplinetype_id)

@strawberry.type
class AdmissionGQLModel:
    id: uuid.UUID
    name: str
    name_en: typing.Optional[str]
    description: typing.Optional[str]
    valid: bool
    created: datetime.datetime
    lastchange: datetime.datetime
    # Additional fields and relationships...

@strawberry.type
class StudentAdmissionGQLModel:
    id: uuid.UUID
    admission: AdmissionGQLModel
    user_id: uuid.UUID
    state: str
    valid: bool
    created: datetime.datetime
    lastchange: datetime.datetime
    # Additional fields and relationships...
