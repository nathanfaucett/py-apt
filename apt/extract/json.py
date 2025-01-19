from typing import Generic, TypeVar, get_args
from msgspec import Struct, json, MsgspecError
from aiohttp.web import Request, Response
from result import Err, Result, Ok

from apt.extract.extract import Extract

T = TypeVar("T", bound=Struct)


class JSON(Generic[T], Extract[Response]):
    value: T

    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value

    @staticmethod
    async def extract(cls, request: Request) -> Result["JSON[T]", Response]:
        try:
            json_type = get_args(cls)[0]
            value = json.decode(await request.read(), type=json_type)
            return Ok(JSON(value))
        except MsgspecError as err:
            return Err(Response(status=400, text=str(err)))

    @staticmethod
    def into_openapi(cls):
        json_type = get_args(cls)[0]
