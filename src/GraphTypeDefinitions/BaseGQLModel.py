import uuid
import strawberry


class BaseGQLModel:
    @classmethod
    def get_table_resolvers(cls):
        raise NotImplementedError()

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        raise NotImplementedError()

    @classmethod
    def from_sqlalchemy(cls, db_row):
        keyed_resolvers = cls.get_table_resolvers()
        instance_values = {
            name: resolver(db_row)
            for name, resolver in keyed_resolvers.items()
        } if db_row is not None else {}

        # print(f"{cls}, {instance_values}", flush=True)
        instance = cls(**instance_values) if db_row is not None else None
        return instance

    @classmethod
    async def load_with_loader(cls, info: strawberry.types.Info, id: uuid.UUID):
        loader = cls.getLoader(info=info)
        db_row = await loader.load(id)
        return cls.from_sqlalchemy(db_row=db_row)

    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
        if id is None: return None
        loader = cls.getLoader(info)
        if isinstance(id, str): id = uuid.UUID(id)
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
        return result