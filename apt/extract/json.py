from msgspec import Struct, json, MsgspecError
from typing import Generic, TypeVar, get_args
from aiohttp.web import Request, Response
from result import Err, Result, Ok

from apt.extract.extract import Extract

T = TypeVar("T", bound=Struct)


class JSON(Generic[T], Extract):
    value: T

    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value

    @staticmethod
    async def extract(cls, request: Request) -> Result["JSON[T]", Response]:
        if request.has_body:
            try:
                json_type = get_args(cls)[0]
                value = json.decode(await request.read(), type=json_type)
                result = JSON[T](value)
                return Ok(result)
            except MsgspecError as err:
                return Err(Response(text=str(err), status=400))
        return Err(Response(status=400))
