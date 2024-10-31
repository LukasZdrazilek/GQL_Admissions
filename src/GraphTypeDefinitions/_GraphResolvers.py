import strawberry
import uuid
import datetime
import typing
from src.GraphPermissions import OnlyForAuthentized

UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".externals")]
GrantingGQLModel = typing.Annotated["GrantingGQLModel", strawberry.lazy(".externals")]

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

async def resolve_user(info, user_id):
    from .externals import UserGQLModel
    result = None if user_id is None else await UserGQLModel.resolve_reference(info, user_id)
    return result

@strawberry.field(description="""User ID """, permission_classes=[OnlyForAuthentized()])
async def resolve_user_id(self, info) -> typing.Optional["UserGQLModel"]:
    return await resolve_user(info, self.user_id)

#################################################### TEST GRANTING #####################################################
async def resolve_program(info, program_id):
    from .externals import GrantingGQLModel
    result = None if program_id is None else await GrantingGQLModel.resolve_reference(info, program_id)
    return result

@strawberry.field(description="""Granting ID """, permission_classes=[OnlyForAuthentized()])
async def resolve_program_id(self, info) -> typing.Optional["GrantingGQLModel"]:
    return await resolve_user(info, self.program_id)
########################################################################################################################

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