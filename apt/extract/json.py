from typing import Generic, TypeVar, Unpack, get_args
from pydantic import BaseModel, ValidationError
from aiohttp.web import Response
from result import Err, Result, Ok

from apt.extract.extract import Extract, ExtractIntoOpenAPIKWArgs, ExtractKWArgs
from apt.openapi import get_or_create_schema

T = TypeVar("T", bound=BaseModel)


class JSON(Generic[T], Extract[Response]):
    value: T

    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value

    @staticmethod
    async def extract(
        cls, **kwargs: Unpack[ExtractKWArgs]
    ) -> Result["JSON[T]", Response]:
        request = kwargs["request"]
        try:
            json_type = get_args(cls)[0]
            value = json_type.model_validate_json(await request.read())
            return Ok(JSON(value))
        except ValidationError as err:
            return Err(Response(status=400, text=err.json()))

    @staticmethod
    def into_openapi(cls, **kwargs: Unpack[ExtractIntoOpenAPIKWArgs]):
        openapi_route = kwargs["openapi_route"]
        openapi = kwargs["openapi"]
        types = kwargs["types"]

        json_type = get_args(cls)[0]
        schema = get_or_create_schema(json_type, openapi, types)
        if "requestBody" not in openapi_route:
            openapi_route["requestBody"] = {"content": {}}
        if "application/json" not in openapi_route["requestBody"]["content"]:
            openapi_route["requestBody"]["content"]["application/json"] = {}

        openapi_route["requestBody"]["content"]["application/json"]["schema"] = schema
