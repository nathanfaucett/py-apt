from typing import (
    Any,
    Dict,
    Generic,
    TypeVar,
    Unpack,
    cast,
    get_args,
    get_origin,
    get_type_hints,
)
from aiohttp import BodyPartReader
from aiohttp.web import Response
from aiohttp.hdrs import CONTENT_DISPOSITION
from result import Err, Result, Ok

from apt import dict_from_form_data
from apt.extract.extract import Extract, ExtractIntoOpenAPIKWArgs, ExtractKWArgs
from apt.openapi import get_or_create_schema
from apt.openapi.spec import OpenAPIBinaryFormat


T = TypeVar("T")


class Multipart(Generic[T], Extract[Response]):
    value: T

    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value

    @staticmethod
    async def extract(
        cls, **kwargs: Unpack[ExtractKWArgs]
    ) -> Result["Multipart", Response]:
        request = kwargs["request"]
        try:
            multipart_type = get_args(cls)[0]
            multipart_type_types = {
                key: item_cls
                for key, item_cls in get_type_hints(multipart_type).items()
            }
            multipart_value = multipart_type()
            reader = await request.multipart()
            while True:
                part = cast(BodyPartReader | None, await reader.next())
                if part is None:
                    break
                content_disposition = dict_from_form_data(
                    part.headers.get(CONTENT_DISPOSITION)
                )
                name = content_disposition.get("name")
                if name is None:
                    continue
                part_type = multipart_type_types.get(name)
                if part_type is bytes:
                    setattr(multipart_value, name, await part.read(decode=False))
                elif part_type is str or part_type is OpenAPIBinaryFormat:
                    setattr(multipart_value, name, await part.text())
            return Ok(Multipart(multipart_value))
        except BaseException as err:
            return Err(Response(status=400, text=str(err)))

    @staticmethod
    def into_openapi(cls, **kwargs: Unpack[ExtractIntoOpenAPIKWArgs]):
        openapi_route = kwargs["openapi_route"]
        openapi = kwargs["openapi"]
        types = kwargs["types"]

        multipart_type = get_args(cls)[0]
        schema = get_or_create_schema(multipart_type, openapi, types)
        if "requestBody" not in openapi_route:
            openapi_route["requestBody"] = {"content": {}}
        if "multipart/form-data" not in openapi_route["requestBody"]["content"]:
            openapi_route["requestBody"]["content"]["multipart/form-data"] = {}

        openapi_route["requestBody"]["content"]["multipart/form-data"][
            "schema"
        ] = schema
