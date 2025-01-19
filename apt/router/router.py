from typing import Any, Callable, Coroutine, Dict, Iterable, List, Union
from aiohttp.web import Response, AbstractRouteDef

from apt.openapi import OpenAPIPath, OpenAPISchema
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
        routes: List[AbstractRouteDef] = []
        prefix = self.get_prefix(prefix)
        for child in self.children:
            if isinstance(child, Router):
                routes.extend(child.into_routes(prefix))
            else:
                routes.append(child.into_route(prefix))
        return routes

    def into_openapi(
        self, components: Dict[str, OpenAPISchema], prefix: str | None = None
    ) -> Dict[str, OpenAPIPath]:
        openapi_paths: Dict[str, OpenAPIPath] = {}
        prefix = self.get_prefix(prefix)
        for child in self.children:
            if isinstance(child, Router):
                for path, method in child.into_openapi(components, prefix).items():
                    if path in openapi_paths:
                        openapi_paths[path].update(method)
                    else:
                        openapi_paths[path] = method
            else:
                for path, method in child.into_openapi(components, prefix).items():
                    if path in openapi_paths:
                        openapi_paths[path].update(method)
                    else:
                        openapi_paths[path] = method
        return openapi_paths
