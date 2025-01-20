from json import dumps
from typing import Dict, Generic, TypeVar, get_args, Type
from msgspec import Struct, MsgspecError, json
from aiohttp.web import Request, Response
from multidict import MultiDictProxy
from result import Err, Result, Ok

from apt.extract.extract import Extract
from apt.openapi import OpenAPI, OpenAPIRoute, get_or_create_component
from apt.util import str_to_python_value

T = TypeVar("T", bound=Struct)


class Query(Generic[T], Extract[Response]):
    value: T

    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value

    @staticmethod
    async def extract(cls, request: Request, path: str) -> Result["Query[T]", Response]:
        try:
            query_type = get_args(cls)[0]
            value = Query.struct_from_query_string(request.url.query, query_type)
            return Ok(Query(value))
        except MsgspecError as err:
            return Err(Response(status=400, text=str(err)))

    @staticmethod
    def into_openapi(
        cls,
        name: str,
        openapi_route: OpenAPIRoute,
        openapi: OpenAPI,
        types: Dict[Type, str],
        path: str
    ):
        query_type = get_args(cls)[0]
        schema = get_or_create_component(query_type, openapi, types)
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
