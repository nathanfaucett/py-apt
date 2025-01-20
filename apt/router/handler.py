from inspect import isclass
from logging import warning
from typing import Any, Callable, Coroutine, Dict, Type
from aiohttp.web import (
    get,
    head,
    post,
    delete,
    put,
    patch,
    options,
    Request,
    Response,
    AbstractRouteDef,
)
from result import Ok, Result, is_err

from apt.extract.extract import Extract
from apt.openapi import (
    OpenAPI,
    OpenAPIRoute,
    OpenAPIBody,
    OpenAPIMethod,
    get_or_create_component,
    is_primitive_schema,
    type_to_schema,
)
from apt.router.endpoint import (
    EndpointOptions,
    endpoint_body_into_openapi,
    get_endpoint_options,
)


class Handler:
    handler: Callable[..., Coroutine[Any, Any, Response]]

    def __init__(self, handler: Callable[..., Coroutine[Any, Any, Response]]):
        self.handler = handler

    def get_endpoint_options(self) -> EndpointOptions:
        return get_endpoint_options(self.handler)

    def get_path(self, prefix: str | None = None) -> str:
        if prefix is not None:
            return f"{prefix}{self.get_endpoint_options()['path']}"
        return self.get_endpoint_options()["path"]

    def get_method(self) -> OpenAPIMethod:
        return self.get_endpoint_options()["method"]

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
            case "options":
                return options(self.get_path(prefix), self.into_handle())
        warning(f"Unknown method: {method}")
        return get(self.get_path(prefix), self.into_handle())

    def into_openapi(
        self,
        openapi: OpenAPI,
        types: Dict[Type, str] | None = None,
        prefix: str | None = None,
    ) -> OpenAPI:
        if types is None:
            types = {}
        path = self.get_path(prefix)
        method = self.get_method()
        endpoint_options = self.get_endpoint_options()
        openapi_route: OpenAPIRoute
        if hasattr(endpoint_options, "openapi"):
            openapi_route = {}
            endpoint_options["openapi"] = openapi_route
        else:
            openapi_route = endpoint_options["openapi"]
        request_body = endpoint_options.get("request_body")
        if request_body is not None:
            openapi_route["requestBody"] = endpoint_body_into_openapi(
                request_body, openapi, types
            )
        responses = endpoint_options.get("responses")
        if responses is not None:
            if "responses" not in openapi_route:
                openapi_route["responses"] = {}
            for status_code, response in responses.items():
                openapi_route["responses"][status_code] = endpoint_body_into_openapi(
                    response, openapi, types
                )

        if "paths" not in openapi:
            openapi["paths"] = {}

        if path not in openapi["paths"]:
            openapi["paths"][path] = {}

        if method not in openapi["paths"][path]:
            openapi["paths"][path][method] = openapi_route
        else:
            openapi["paths"][path][method].update(openapi_route)

        return openapi
