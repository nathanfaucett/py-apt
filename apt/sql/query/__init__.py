from typing import Generic, TypeVar


T = TypeVar("T")


class QueryResult(str, Generic[T]):
    return_value: T

    def __new__(cls, string: str, return_value: T):
        instance = super().__new__(cls, string)
        instance.__init__(string, return_value)
        return instance

    def __init__(self, string: str, return_value: T):
        self.return_value = return_value

    def get_return_value(self) -> T:
        return self.return_value
