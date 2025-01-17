from typing import Any, Dict, List, Literal, Tuple, Type, TypedDict, Union


OpenAPIIn = Union[Literal["path"], Literal["header"]]


class OpenAPIResponseDict(TypedDict):
    content_type: str | None
    format: str | None
    example: str | None
    type: Type | None
    schema: Any | None


OpenAPIResponse = Union[Type, Tuple[str, Type], OpenAPIResponseDict]

OpenAPIResponses = Dict[int, OpenAPIResponse]


class OpenAPIParameterDict(TypedDict):
    name: str
    inside: OpenAPIIn | None
    description: str | None
    required: Literal[True] | None
    type: Type | None
    schema: Any | None


OpenAPIParameters = List[OpenAPIParameterDict]


__openapi_attr_key__ = "__openapi__"


class OpenAPIRoute(TypedDict):
    tags: List[str] | None
    summary: str | None
    description: str | None
    operationId: str | None
    parameters: OpenAPIParameters | None
    responses: OpenAPIResponses | None
    externalDocs: Dict[str, Any] | None
