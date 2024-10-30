import strawberry
from datetime import datetime
from typing import Optional

@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing an admission entry for a specific course with associated metadata""",
)
class AdmissionGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        if id is None:
            return None

        # Assuming this is where you would implement database fetching logic
        result = {
            "id": id,
            "name": "Sample Name",
            "name_en": "Sample English Name",
            "description": "Sample description",
            "course_id": "course-id-example",
            "startdate": datetime.now(),
            "enddate": datetime.now(),
            "valid": True,
            "created": datetime.now(),
            "lastchange": datetime.now(),
            "createdby": "user-id-example",
            "changedby": "user-id-example",
            "rbacobject": "user-group-id-example"
        }
        
        return result

    @strawberry.field(description="Primary key")
    def id(self) -> strawberry.ID:
        return self["id"]

    @strawberry.field(description="Name of the admission entry")
    def name(self) -> str:
        return self["name"]

    @strawberry.field(description="English name of the admission entry")
    def name_en(self) -> str:
        return self["name_en"]

    @strawberry.field(description="Description of the admission entry")
    def description(self) -> str:
        return self["description"]

    @strawberry.field(description="Foreign key referencing the associated course")
    def course_id(self) -> str:
        return self["course_id"]

    @strawberry.field(description="Admission validity start date")
    def startdate(self) -> Optional[datetime]:
        return self["startdate"]

    @strawberry.field(description="Admission validity end date")
    def enddate(self) -> Optional[datetime]:
        return self["enddate"]

    @strawberry.field(description="Indicates if the admission entry is valid")
    def valid(self) -> bool:
        return self["valid"]

    @strawberry.field(description="Timestamp when the admission entry was created")
    def created(self) -> datetime:
        return self["created"]

    @strawberry.field(description="Timestamp of the last change to the admission entry")
    def lastchange(self) -> datetime:
        return self["lastchange"]

    @strawberry.field(description="User ID of the creator")
    def createdby(self) -> Optional[str]:
        return self["createdby"]

    @strawberry.field(description="User ID of the last modifier")
    def changedby(self) -> Optional[str]:
        return self["changedby"]

    @strawberry.field(description="User or group ID that controls access to the admission entry")
    def rbacobject(self) -> Optional[str]:
        return self["rbacobject"]

@strawberry.field(description="Returns an admission entry by ID")
async def admission_by_id(info: strawberry.types.Info, id: strawberry.ID) -> AdmissionGQLModel:
    return await AdmissionGQLModel.resolve_reference(info, id)
