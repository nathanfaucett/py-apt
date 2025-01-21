from typing import Any, Callable, Coroutine, Iterable, Type, Union
from aiohttp.web import Response, AbstractRouteDef

from apt.openapi.spec import OpenAPI
from apt.router.handler import Handler


class Router:
    prefix: str
    children: list[Union[Handler, "Router"]]

    def __init__(self, prefix: str | None = None):
        if prefix is not None:
            self.prefix = prefix
        else:
            self.prefix = ""
        self.children = []

    def get_prefix(self, prefix: str | None = None) -> str:
        if prefix is None:
            return self.prefix
        return prefix + self.prefix

    def add(
        self,
        child: Union[Callable[..., Coroutine[Any, Any, Response]], Handler, "Router"],
    ) -> "Router":
        if isinstance(child, Handler):
            self.children.append(child)
        elif isinstance(child, Router):
            self.children.append(child)
        elif callable(child):
            self.children.append(Handler(child))
        return self

    def into_routes(self, prefix: str | None = None) -> Iterable[AbstractRouteDef]:
        routes: list[AbstractRouteDef] = []
        prefix = self.get_prefix(prefix)
        for child in self.children:
            if isinstance(child, Router):
                routes.extend(child.into_routes(prefix))
            else:
                routes.append(child.into_route(prefix))
        return routes

    def into_openapi(
        self,
        openapi: OpenAPI,
        types: dict[Type, str] | None = None,
        prefix: str | None = None,
    ) -> OpenAPI:
        prefix = self.get_prefix(prefix)
        if types is None:
            types = {}
        for child in self.children:
            openapi = child.into_openapi(openapi, types, prefix)
        return openapi
