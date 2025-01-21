from abc import ABC, abstractmethod
from typing import Any, Generic, Type, TypeGuard, TypeVar, TypedDict, Unpack
from aiohttp.web import Request
from result import Result

from apt.openapi import OpenAPI
from apt.openapi.spec import OpenAPIRoute


E = TypeVar("E")


class ExtractKWArgs(TypedDict):
    request: Request
    path_pattern: str


class ExtractIntoOpenAPIKWArgs(TypedDict):
    name: str
    openapi_route: OpenAPIRoute
    openapi: OpenAPI
    types: dict[Type, str]
    path_pattern: str


class Extract(ABC, Generic[E]):

    @staticmethod
    def is_extractor(cls: Any) -> TypeGuard["Extract"]:
        return cls is not None and hasattr(cls, "extract") and callable(cls.extract)

    @staticmethod
    @abstractmethod
    async def extract(cls, **kwargs: Unpack[ExtractKWArgs]) -> Result["Extract", E]: ...

    @staticmethod
    @abstractmethod
    def into_openapi(cls, **kwargs: Unpack[ExtractIntoOpenAPIKWArgs]):
        pass
