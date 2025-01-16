__http_options_attr_key__ = "__http_options__"


class HandlerOptions:
    def __init__(self):
        self.path = ""
        self.method = "GET"

    @staticmethod
    def get(func) -> "HandlerOptions":
        if not hasattr(func, __http_options_attr_key__):
            setattr(func, __http_options_attr_key__, HandlerOptions())
        return getattr(func, __http_options_attr_key__)

    def __str__(self):
        return f"HandlerOptions(path={self.path}, method={self.method})"
