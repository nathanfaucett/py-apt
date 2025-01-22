from json import dumps
from typing import Generic, TypeVar, Unpack, get_args, Type
from msgspec import Struct, MsgspecError, json
from aiohttp.web import Response
from multidict import MultiDictProxy
from result import Err, Result, Ok

from apt.extract.extract import Extract, ExtractIntoOpenAPIKWArgs, ExtractKWArgs
from apt.openapi import get_or_create_schema
from apt import str_to_python_value

T = TypeVar("T", bound=Struct)


class Query(Generic[T], Extract[Response]):
    value: T

    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value

    @staticmethod
    async def extract(
        cls, **kwargs: Unpack[ExtractKWArgs]
    ) -> Result["Query[T]", Response]:
        request = kwargs["request"]
        try:
            query_type = get_args(cls)[0]
            value = Query.struct_from_query_string(request.url.query, query_type)
            return Ok(Query(value))
        except MsgspecError as err:
            return Err(Response(status=400, text=str(err)))

    @staticmethod
    def into_openapi(cls, **kwargs: Unpack[ExtractIntoOpenAPIKWArgs]):
        openapi_route = kwargs["openapi_route"]
        openapi = kwargs["openapi"]
        types = kwargs["types"]
        name = kwargs["name"]

        query_type = get_args(cls)[0]
        schema = get_or_create_schema(query_type, openapi, types)
        if "parameters" not in openapi_route:
            openapi_route["parameters"] = []
        openapi_route["parameters"].append(
            {
                "in": "query",
                "name": name,
                "schema": schema,
            }
        )

    @staticmethod
    def struct_from_query_string(query: MultiDictProxy[str], query_type: Type[T]) -> T:
        args = {}
        for key, value in query.items():
            if isinstance(value, str):
                args[key] = str_to_python_value(value[0])
            else:
                args[key] = [str_to_python_value(element) for element in value]
        return json.decode(dumps(args), type=query_type)
