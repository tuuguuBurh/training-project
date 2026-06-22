from fastapi import APIRouter

from app.v1 import auth, leave_requests

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(
    leave_requests.leave_types_router,
    prefix="/leave-types",
    tags=["Leave Types"],
)
api_router.include_router(
    leave_requests.router,
    prefix="/leave-requests",
    tags=["Leave Requests"],
)
