from typing import Any, Callable, Coroutine, Iterable, Union
from aiohttp.web import Response, AbstractRouteDef

from apt.router.handler import Handler


class Router:
    handlers: list[Handler] = list()

    def __init__(self):
        pass

    def add(
        self, handle: Union[Callable[..., Coroutine[Any, Any, Response]], Handler]
    ) -> "Router":
        if isinstance(handle, Handler):
            self.handlers.append(handle)
        elif callable(handle):
            self.handlers.append(Handler(handle))
        return self

    def into_routes(self) -> Iterable[AbstractRouteDef]:
        return [handler.into_route() for handler in self.handlers]
