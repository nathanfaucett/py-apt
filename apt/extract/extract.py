from abc import ABC, abstractmethod
from typing import Any, Generic, TypeGuard, TypeVar
from aiohttp.web import Request
from result import Result

E = TypeVar("E")


class Extract(ABC, Generic[E]):

    @staticmethod
    def is_extractor(cls: Any) -> TypeGuard["Extract"]:
        return hasattr(cls, "extract") and callable(cls.extract)

    @staticmethod
    @abstractmethod
    async def extract(cls, request: Request) -> Result["Extract", E]: ...
