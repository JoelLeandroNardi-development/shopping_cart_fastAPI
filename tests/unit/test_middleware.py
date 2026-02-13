import asyncio
import json

from fastapi.responses import JSONResponse

from app.middleware import register_middleware
from app.core.exceptions import NotFoundException

class DummyApp:
    def __init__(self):
        self._middleware = None

    def middleware(self, _type):
        def decorator(fn):
            self._middleware = fn
            return fn

        return decorator

def _get_middleware():
    app = DummyApp()
    register_middleware(app)
    return app._middleware

async def _call_next_ok(request):
    return JSONResponse(status_code=200, content={"ok": True})

async def _call_next_notfound(request):
    raise NotFoundException("missing")

async def _call_next_valueerror(request):
    raise ValueError("bad input")

async def _call_next_generic(request):
    raise Exception("boom")

def _run(coro):
    return asyncio.run(coro)

def test_exception_middleware_various_cases():
    middleware = _get_middleware()

    cases = [
        (_call_next_ok, 200, {"ok": True}),
        (_call_next_notfound, 404, {"detail": "missing"}),
        (_call_next_valueerror, 400, {"detail": "bad input"}),
        (_call_next_generic, 500, {"detail": "Internal Server Error"}),
    ]

    for call_next, expected_status, expected_body in cases:
        response = _run(middleware(None, call_next))
        assert isinstance(response, JSONResponse)
        assert response.status_code == expected_status
        body = json.loads(response.body)
        assert body == expected_body
