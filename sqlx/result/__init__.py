from typing import Generic, TypeVar


A = TypeVar("A", bound=tuple)
R = TypeVar("R")


class SQLxResult(str, Generic[A, R]):
    arguments: A
    returns: R

    def __new__(cls, string: str, arguments: A, returns: R):
        instance = super().__new__(cls, string)
        instance.__init__(string, arguments, returns)
        return instance

    def __init__(self, string: str, arguments: A, returns: R):
        self.arguments = arguments
        self.returns = returns
