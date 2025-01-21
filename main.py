# import os
# import asyncio
# from contextlib import asynccontextmanager
# from fastapi import FastAPI, Request
# from fastapi.responses import FileResponse
# from strawberry.fastapi import GraphQLRouter
#
# from src.GraphTypeDefinitions import schema
#
# appcontext = {}
# @asynccontextmanager
# async def initEngine(app: FastAPI):
#
#     from src.DBDefinitions import startEngine, ComposeConnectionString
#
#     connectionstring = ComposeConnectionString()
#
#     asyncSessionMaker = await startEngine(
#         connectionstring=connectionstring,
#         makeDrop=True,
#         makeUp=True
#     )
#
#     appcontext["asyncSessionMaker"] = asyncSessionMaker
#     print("engine started", flush=True)
#     yield
#
#
# app = FastAPI(lifespan=initEngine)
#
# print("All initialization is done ")
#
# @app.get('/hello')
# def hello():
#    return {'hello': 'world'}
#
# graphql_app = GraphQLRouter(schema)
# app.include_router(graphql_app, prefix="/gql")

import os
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager

from src.DBDefinitions import startEngine, ComposeConnectionString
from src.GraphTypeDefinitions import schema

connectionString = ComposeConnectionString()


def singleCall(asyncFunc):
    """Dekorator, ktery dovoli, aby dekorovana funkce byla volana (vycislena) jen jednou. Navratova hodnota je zapamatovana a pri dalsich volanich vracena.
    Dekorovana funkce je asynchronni.
    """
    resultCache = {}

    async def result():
        if resultCache.get("result", None) is None:
            resultCache["result"] = await asyncFunc()
        return resultCache["result"]

    return result


@singleCall
async def RunOnceAndReturnSessionMaker():
    """Provadi inicializaci asynchronniho db engine, inicializaci databaze a vraci asynchronni SessionMaker.
    Protoze je dekorovana, volani teto funkce se provede jen jednou a vystup se zapamatuje a vraci se pri dalsich volanich.
    """

    makeDrop = os.getenv("DEMO", None) == "True"
    # logging.info(f'starting engine for "{connectionString} makeDrop={makeDrop}"')

    initizalizedEngine = await startEngine(
        connectionstring=connectionString, makeDrop=makeDrop, makeUp=True
    )

    async def initDBWithReport(initizalizedEngine):
        from src.utils.DBFeeder import initDB
        await initDB(initizalizedEngine)
        print("data initialized", flush=True)

    future = initDBWithReport(initizalizedEngine)
    asyncio.create_task(future)
    return initizalizedEngine


async def get_context(request: Request):
    asyncSessionMaker = await RunOnceAndReturnSessionMaker()

    from src.utils.Dataloaders import createLoadersContext
    context = createLoadersContext(asyncSessionMaker)
    result = {**context}
    result["request"] = request
    return result


@asynccontextmanager
async def lifespan(app: FastAPI):
    initizalizedEngine = await RunOnceAndReturnSessionMaker()
    yield


app = FastAPI(lifespan=lifespan)

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)

app.include_router(graphql_app, prefix="/gql")


@app.get("/voyager", response_class=FileResponse)
async def graphiql():
    realpath = os.path.realpath("./voyager.html")
    return realpath