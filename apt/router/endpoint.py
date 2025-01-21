from inspect import isclass
from typing import (
    Any,
    NotRequired,
    TypeGuard,
    TypedDict,
    Type,
    Union,
)

from apt.openapi import (
    OpenAPIBody,
    OpenAPIRoute,
    OpenAPIMethod,
    OpenAPISchemaArray,
    OpenAPI,
    get_or_create_component,
)
from apt import to_camel_case

__endpoint_options_attr_key__ = "__endpoint_options__"


class EndpointBodyDict(TypedDict):
    content_type: NotRequired[str]
    type: NotRequired[Type]
    description: NotRequired[str]
    example: NotRequired[Any]
    nullable: NotRequired[bool]
    read_only: NotRequired[bool]
    write_only: NotRequired[bool]
    # strings
    format: NotRequired[str]
    enum: NotRequired[list[str]]
    default: NotRequired[Any]
    pattern: NotRequired[str]
    min_length: NotRequired[int]
    max_length: NotRequired[int]
    # numbers
    minimum: NotRequired[Union[int, float]]
    maximum: NotRequired[Union[int, float]]
    exclusive_minimum: NotRequired[bool]
    exclusive_maximum: NotRequired[bool]
    multiple_of: NotRequired[Union[int, float]]
    # arrays
    items: NotRequired[Type]
    unique_items: NotRequired[bool]
    min_items: NotRequired[int]
    max_items: NotRequired[int]
    # objects
    properties: NotRequired[dict[str, Type]]
    additional_properties: NotRequired[Union[Type, bool]]
    required: NotRequired[list[str]]


def is_array_endpoint_key(key: str) -> bool:
    return key in ["items", "unique_items", "min_items", "max_items"]


def is_type_endpoint_key(key: str) -> bool:
    return key in ["type", "items", "content_type"]


def is_endpoint_body_dict(obj) -> TypeGuard[EndpointBodyDict]:
    return isinstance(obj, dict) and (
        isclass(obj.get("type")) or isclass(obj.get("items"))
    )


EndpointBody = Union[Type, tuple[str, Type], EndpointBodyDict, OpenAPIBody]
EndpointResponses = dict[int, EndpointBody]


def endpoint_body_into_openapi(
    endpoint_body: EndpointBody, openapi: OpenAPI, types: dict[Type, str]
) -> OpenAPIBody:
    if isclass(endpoint_body):
        return {
            "content": {
                "application/json": {
                    "schema": get_or_create_component(endpoint_body, openapi, types)
                }
            }
        }
    elif isinstance(endpoint_body, tuple):
        content_type = endpoint_body[0]
        return {
            "content": {
                content_type: {
                    "schema": get_or_create_component(endpoint_body[1], openapi, types)
                }
            }
        }
    elif is_endpoint_body_dict(endpoint_body):
        content_type = endpoint_body.get("content_type", "application/json")
        endpoint_type: Type
        is_array = False
        if "type" in endpoint_body:
            endpoint_type = endpoint_body["type"]
        elif "items" in endpoint_body:
            endpoint_type = endpoint_body["items"]
            is_array = True
        schema = get_or_create_component(endpoint_type, openapi, types)
        openapi_schema = schema
        if is_array:
            openapi_schema = OpenAPISchemaArray(
                type="array",
                items=schema,
            )

        for key, value in endpoint_body.items():
            if is_type_endpoint_key(key):
                continue

            if is_array_endpoint_key(key):
                openapi_schema[to_camel_case(key)] = value
            else:
                schema[to_camel_case(key)] = value

        return {"content": {content_type: {"schema": openapi_schema}}}
    else:
        return endpoint_body


class EndpointOptions(TypedDict):
    path: str
    method: OpenAPIMethod
    description: NotRequired[str]
    responses: NotRequired[EndpointResponses]
    request_body: NotRequired[EndpointBody]
    openapi: NotRequired[OpenAPIRoute]


def get_endpoint_options(func) -> EndpointOptions:
    if not hasattr(func, __endpoint_options_attr_key__):
        setattr(func, __endpoint_options_attr_key__, {"openapi": {}})
    return getattr(func, __endpoint_options_attr_key__)


def endpoint(
    path: str,
    method: str,
    responses: EndpointResponses | None = None,
    request_body: EndpointBody | None = None,
    openapi: OpenAPIRoute | None = None,
):
    def wrapper(func):
        endpoint_options = get_endpoint_options(func)
        endpoint_options["path"] = path
        endpoint_options["method"] = method.lower()
        if responses is not None:
            endpoint_options["responses"] = responses
        if request_body is not None:
            endpoint_options["request_body"] = request_body
        if openapi is not None:
            endpoint_options["openapi"] = openapi
        return func

    return wrapper
