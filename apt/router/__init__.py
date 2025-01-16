from apt.router.handler_options import HandlerOptions


def method(http_method: str):
    def handler(func):
        HandlerOptions.get(func).method = http_method
        return func

    return handler


def path(http_path: str):
    def handler(func):
        HandlerOptions.get(func).path = http_path
        return func

    return handler
