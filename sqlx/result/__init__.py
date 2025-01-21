from typing import Generic, TypeVar


A = TypeVar("A")
R = TypeVar("R")


class SQLxResult(str, Generic[A, R]):
    def __new__(cls, string: str):
        return super().__new__(cls, string)
