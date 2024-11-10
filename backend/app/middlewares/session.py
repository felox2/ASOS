import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

SESSION_COOKIE_NAME = "session_id"

class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        session_id = request.cookies.get(SESSION_COOKIE_NAME)
        if not session_id:
            session_id = str(uuid.uuid4())
            response = await call_next(request)
            response.set_cookie(SESSION_COOKIE_NAME, session_id)
            return response
        request.state.session_id = session_id
        response = await call_next(request)
        return response