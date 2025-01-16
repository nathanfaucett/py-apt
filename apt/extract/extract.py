from abc import ABC, abstractmethod
from typing import Any, Type, TypeGuard
from aiohttp.web import Request, Response
from result import Result


class Extract(ABC):

    @staticmethod
    def has_extract(cls: Any) -> TypeGuard["Extract"]:
        return hasattr(cls, "extract") and callable(cls.extract)

    @staticmethod
    @abstractmethod
    async def extract(cls, request: Request) -> Result["Extract", Response]:
        pass
