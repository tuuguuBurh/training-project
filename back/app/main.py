import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.middelwares.db_session import DBSessionMiddleware
from app.v1.api_user import user_router

log_fmt = "%(pathname)s:%(funcName)s(%(lineno)d) %(message)s"
logging.basicConfig(
    format="%(levelname)s " + log_fmt,
    level=logging.DEBUG if settings.ENV == "local" else logging.INFO,
)


def get_application():
    _debug = settings.ENV == "local"
    _app = FastAPI(
        debug=_debug,
        title=settings.PROJECT_NAME,
        openapi_url=settings.OPENAPI_URL,
    )
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return _app


app = get_application()
app.add_middleware(DBSessionMiddleware)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(user_router, prefix=settings.API_V1_STR)
