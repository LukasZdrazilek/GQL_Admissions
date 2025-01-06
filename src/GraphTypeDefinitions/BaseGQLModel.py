from uuid import UUID
import datetime
import typing
import strawberry
import dataclasses

from uoishelpers.gqlpermissions import OnlyForAuthentized, RBACObjectGQLModel

UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]

@classmethod
async def resolve_reference(cls, info: strawberry.types.Info, id: UUID, **otherData):
    _id = UUID(id) if isinstance(id, str) else id
    return None if id is None else cls(id=_id, **otherData)

@strawberry.federation.interface(
    keys=["id"], description="""Entity representing an interface"""
)
class BaseGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        raise NotImplementedError()

    @classmethod
    def from_dataclass(cls, db_row):
        db_row_dict = dataclasses.asdict(db_row)
        instance = cls(**db_row_dict)
        return instance

    @classmethod
    async def load_with_loader(cls, info: strawberry.types.Info, id: UUID):
        if id is None: return None

        _id = UUID(id) if isinstance(id, str) else id
        loader = cls.getLoader(info=info)
        db_row = await loader.load(_id)

        return None if db_row is None else cls.from_dataclass(db_row=db_row)

    @classmethod
    def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
        return cls.load_with_loader(info=info, id=id)

    id: typing.Optional[UUID] = strawberry.field(
        description="primary key",
        default=None,
        # permission_classes=[OnlyForAuthentized]
    )
    lastchange: typing.Optional[datetime.date] = strawberry.field(
        description="timestamp",
        default=None,
        # permission_classes=[OnlyForAuthentized]
    )
    created: typing.Optional[datetime.date] = strawberry.field(
        description="date & time of unit born",
        default=None,
        # permission_classes=[OnlyForAuthentized]
    )
    createdby_id: typing.Optional[UUID] = strawberry.field(
        description="who created this entity",
        default=None,
        # permission_classes=[OnlyForAuthentized]
    )
    changedby_id: typing.Optional[UUID] = strawberry.field(
        description="who changed this entity",
        default=None,
        # permission_classes=[OnlyForAuthentized]
    )
    rbacobject_id: typing.Optional[UUID] = strawberry.field(
        description="rbac ruling object",
        default=None,
        # permission_classes=[OnlyForAuthentized]
    )

    # @classmethod
    # def from_sqlalchemy(cls, db_row):
    #     keyed_resolvers = cls.get_table_resolvers()
    #     instance_values = {
    #         name: resolver(db_row)
    #         for name, resolver in keyed_resolvers.items()
    #     } if db_row is not None else {}
    #
    #     # print(f"{cls}, {instance_values}", flush=True)
    #     instance = cls(**instance_values) if db_row is not None else None
    #     return instance
    #
    # @classmethod
    # async def load_with_loader(cls, info: strawberry.types.Info, id: UUID):
    #     loader = cls.getLoader(info=info)
    #     db_row = await loader.load(id)
    #     return cls.from_sqlalchemy(db_row=db_row)
    #
    # @classmethod
    # async def resolve_reference(cls, info: strawberry.types.Info, id: UUID):
    #     if id is None: return None
    #     loader = cls.getLoader(info)
    #     if isinstance(id, str): id = UUID(id)
    #     result = await loader.load(id)
    #     if result is not None:
    #         result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
    #     return result
    #
    # @classmethod
    # async def load_with_loader(cls, info: strawberry.types.Info, id: UUID):
    #     if id is None: return None
    #
    #     _id = UUID(id) if isinstance(id, str) else id
    #     loader = cls.getLoader(info=info)
    #     db_row = await loader.load(_id)
    #
    #     return None if db_row is None else cls.from_dataclass(db_row=db_row)
    #
    # @classmethod
    # def resolve_reference(cls, info: strawberry.types.Info, id: UUID, **otherdata):
    #     return cls.load_with_loader(info=info, id=id)

    @strawberry.field(
        description="who created this entity",
        # permission_classes=[OnlyForAuthentized]
    )
    async def createdby(self) -> typing.Optional["UserGQLModel"]:
        from .UserGQLModel import UserGQLModel
        return None if self.changedby_id is None else UserGQLModel(id=self.createdby_id)

    @strawberry.field(
        description="who created this entity",
        # permission_classes=[OnlyForAuthentized]
    )
    async def changedby(self) -> typing.Optional["UserGQLModel"]:
        from .UserGQLModel import UserGQLModel
        return None if self.changedby_id is None else UserGQLModel(id=self.changedby_id)

    @strawberry.field(
        description="rbac holds relations of user",
        # permission_classes=[OnlyForAuthentized]
    )
    async def rbacobject(self) -> typing.Optional["RBACObjectGQLModel"]:
        return None if self.rbacobject_id is None else RBACObjectGQLModel(id=self.rbacobject_id)