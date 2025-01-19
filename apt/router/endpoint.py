from typing import Dict, NotRequired, TypedDict, Type, Union, Tuple
from apt.openapi import OpenAPIBody, OpenAPIRoute

__endpoint_options_attr_key__ = "__endpoint_options__"


EndpointBody = Union[Type, Tuple[str, Type], OpenAPIBody]
EndpointResponses = Dict[int, EndpointBody]


class EndpointOptions(TypedDict):
    path: str
    method: str
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
    responses: NotRequired[EndpointResponses] = None,
    request_body: NotRequired[EndpointBody] = None,
    openapi: NotRequired[OpenAPIRoute] = None,
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
