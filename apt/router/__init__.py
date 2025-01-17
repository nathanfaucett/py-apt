from typing import Dict, Type, Union, Tuple
from apt.router.handler_options import HandlerOptions


def method(http_method: str):
    def handler(func):
        HandlerOptions.get(func).method = http_method.lower()
        return func

    return handler


def path(http_path: str):
    def handler(func):
        HandlerOptions.get(func).path = http_path
        return func

    return handler


def response(http_responses: Dict[int, Union[Type, Tuple[str, Type]]]):
    def handler(func):
        HandlerOptions.get(func).responses = http_responses
        return func

    return handler
