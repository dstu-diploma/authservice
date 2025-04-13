from contextlib import asynccontextmanager
from app.views import main_router
from app.grpc.auth import serve
from fastapi import FastAPI
from app.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    server = await serve()
    yield
    await server.stop(grace=None)


app = FastAPI(
    title="DSTU Diploma | AuthService", docs_url="/swagger", lifespan=lifespan
)
init_db(app)
app.include_router(main_router)
