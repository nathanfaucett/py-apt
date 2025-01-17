from logging import warning
from typing import Any, Callable, Coroutine, Dict, Tuple, Type, Union
from aiohttp.web import (
    get,
    head,
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

    def get_options(self) -> HandlerOptions:
        return HandlerOptions.get(self.handler)

    def get_path(self, prefix: str | None = None) -> str:
        if prefix is not None:
            return f"{prefix}{self.get_options().path}"
        return self.get_options().path

    def get_method(self) -> str:
        return self.get_options().method.lower()

    def get_responses(
        self,
    ) -> Dict[int, Union[Type, Tuple[str, Type], Tuple[str, Type, str]]]:
        return self.get_options().responses

    def get_name(self) -> str:
        return self.handler.__name__

    def get_types(self) -> dict[str, Any]:
        return self.handler.__annotations__

    async def arguments(self, request: Request) -> Result[dict[str, Any], Response]:
        args: dict[str, Any] = {}
        for key, cls in self.handler.__annotations__.items():
            if Extract.is_extractor(cls):
                value = await cls.extract(cls, request)
                if is_err(value):
                    return value
                args[key] = value.ok()
            elif key == "return":
                continue
            elif key == "request":
                args[key] = request
            else:
                print(f"Unknown type: {cls}")
        return Ok(args)

    async def handle(self, request: Request) -> Response:
        result = await self.arguments(request)
        if is_err(result):
            error = result.err()
            if isinstance(error, Response):
                return error
            return Response(status=500, text=str(error))
        else:
            args = result.ok() or dict(request=request)
            return await self.handler(**args)

    def into_handle(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        async def handle(request: Request) -> Response:
            return await self.handle(request)

        return handle

    def into_route(self, prefix: str | None = None) -> AbstractRouteDef:
        method = self.get_method()
        match method:
            case "get":
                return get(self.get_path(prefix), self.into_handle())
            case "post":
                return post(self.get_path(prefix), self.into_handle())
            case "delete":
                return delete(self.get_path(prefix), self.into_handle())
            case "put":
                return put(self.get_path(prefix), self.into_handle())
            case "patch":
                return patch(self.get_path(prefix), self.into_handle())
            case "head":
                return head(self.get_path(prefix), self.into_handle())
        warning(f"Unknown method: {method}")
        return get(self.get_path(prefix), self.into_handle())
