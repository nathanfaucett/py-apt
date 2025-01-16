from inspect import isclass
from logging import warn
from typing import Any, Callable, Coroutine
from aiohttp.web import (
    get,
    post,
    delete,
    put,
    patch,
    Request,
    Response,
    AbstractRouteDef,
)
from result import Ok, Result, is_err

from apt.extract.extract import Extract
from apt.router.handler_options import HandlerOptions


class Handler:
    def __init__(self, handler: Callable[..., Coroutine[Any, Any, Response]]):
        self.handler = handler

    def options(self) -> HandlerOptions:
        return HandlerOptions.get(self.handler)

    def path(self) -> str:
        return self.options().path

    def method(self) -> str:
        return self.options().method

    async def arguments(self, request: Request) -> Result[dict[str, Any], Response]:
        args: dict[str, Any] = dict()
        for key, cls in self.handler.__annotations__.items():
            if key == "return":
                continue
            elif key == "request":
                args[key] = request
            elif Extract.has_extract(cls):
                value = await cls.extract(cls, request)
                if is_err(value):
                    return value
                args[key] = value.ok()
            else:
                print(f"Unknown type: {cls}")
        return Ok(args)

    async def handle(self, request: Request) -> Response:
        result = await self.arguments(request)
        if is_err(result):
            return result.err()
        else:
            args = result.ok() or dict(request=request)
            return await self.handler(**args)

    def into_handle(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        async def handle(request: Request) -> Response:
            return await self.handle(request)

        return handle

    def into_route(self) -> AbstractRouteDef:
        match self.method():
            case "get":
                return get(self.path(), self.into_handle())
            case "post":
                return post(self.path(), self.into_handle())
            case "delete":
                return delete(self.path(), self.into_handle())
            case "put":
                return put(self.path(), self.into_handle())
            case "patch":
                return patch(self.path(), self.into_handle())
        warn(f"Unknown method: {self.method()}")
        return get(self.path(), self.into_handle())
