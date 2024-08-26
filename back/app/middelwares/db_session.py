from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.db.session import SessionLocal


class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = None
        try:
            request.state.db = SessionLocal()
            response = await call_next(request)
        except Exception as e:
            if request.state.db:
                request.state.db.close()
            raise e
        finally:
            if request.state.db:
                request.state.db.close()
        return response
