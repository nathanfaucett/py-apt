from typing import (
    Generic,
    Iterable,
    TypeVar,
    Unpack,
    get_args,
    Type,
    get_origin,
)
from aiohttp.web import Response
from result import Err, Result, Ok

from apt.extract.extract import Extract, ExtractIntoOpenAPIKWArgs, ExtractKWArgs

from apt.openapi.schema import get_or_create_component
from apt import str_to_python_value

T = TypeVar("T")


class Path(Generic[T], Extract[Response]):
    value: T

    def __init__(self, value: T):
        self.value = value

    def get(self) -> T:
        return self.value

    @staticmethod
    async def extract(
        cls, **kwargs: Unpack[ExtractKWArgs]
    ) -> Result["Path[T]", Response]:
        request = kwargs["request"]
        path_pattern = kwargs["path_pattern"]
        try:
            path_type = get_args(cls)[0]
            value = Path.tuple_from_path(request.path, path_pattern, path_type)
            return Ok(Path(value))
        except Exception as err:
            return Err(Response(status=400, text=str(err)))

    @staticmethod
    def into_openapi(cls, **kwargs: Unpack[ExtractIntoOpenAPIKWArgs]):
        openapi_route = kwargs["openapi_route"]
        openapi = kwargs["openapi"]
        types = kwargs["types"]
        path_pattern = kwargs["path_pattern"]

        path_type = get_args(cls)[0]
        path_types: Iterable[Type]
        if get_origin(path_type) is tuple:
            path_types = get_args(path_type)
        else:
            path_types = [path_type]

        if "parameters" not in openapi_route:
            openapi_route["parameters"] = []

        names = [
            name[1:-1]
            for name in path_pattern.split("/")
            if name.startswith("{") and name.endswith("}")
        ]
        for i, path_type in enumerate(path_types):
            openapi_route["parameters"].append(
                {
                    "in": "path",
                    "name": names[i],
                    "schema": get_or_create_component(path_type, openapi, types),
                }
            )

    @staticmethod
    def tuple_from_path(path: str, path_pattern: str, path_type: Type[T]) -> T:
        path_parts = path.split("/")
        pattern_parts = path_pattern.split("/")

        if len(path_parts) != len(pattern_parts):
            raise ValueError("Path parts and pattern parts do not match")

        path_types: Iterable[Type]
        if get_origin(path_type) is tuple:
            path_types = get_args(path_type)
        else:
            path_types = [path_type]

        path_type_index = 0
        results = []
        for i, pattern_part in enumerate(pattern_parts):
            if pattern_part.startswith("{") and pattern_part.endswith("}"):
                # TODO: use path_type to parse value
                # path_type = path_types[path_type_index]
                # path_type_index += 1
                results.append(str_to_python_value(path_parts[i]))

        if len(results) == 1:
            return results[0]

        return tuple(results)
