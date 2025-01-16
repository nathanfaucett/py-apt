from json import dumps
from msgspec import Struct, MsgspecError, json
from typing import Any, Generic, TypeVar, get_args, Type
from aiohttp.web import Request, Response
from multidict import MultiDictProxy
from result import Err, Result, Ok

from apt.extract.extract import Extract

T = TypeVar("T", bound=Struct)


class Query(Generic[T], Extract):
    value: T

    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value

    @staticmethod
    async def extract(cls, request: Request) -> Result["Query[T]", Response]:
        try:
            query_type = get_args(cls)[0]
            value = struct_from_query_string(request.url.query, query_type)
            result = Query[T](value)
            return Ok(result)
        except MsgspecError as err:
            return Err(Response(text=str(err), status=400))


def struct_from_query_string(query: MultiDictProxy[str], query_type: Type[T]) -> T:
    args = dict()
    for key, value in query.items():
        if len(value) == 1:
            value = value[0]
        args[key] = parse_url_value(value)
    return json.decode(dumps(args), type=query_type)


def parse_url_value(element: Any) -> Any:
    if is_int(element):
        return int(element)
    elif is_float(element):
        return float(element)
    elif element == "true":
        return True
    elif element == "false":
        return False
    else:
        return element


def is_int(element: Any) -> bool:
    if element is None:
        return False
    try:
        int(element)
        return True
    except ValueError:
        return False


def is_float(element: Any) -> bool:
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False
