from typing import Optional, TypeVar

from sqlx.result import SQLxResult


A = TypeVar("A", bound=tuple)
R = TypeVar("R")


def query_one(query: SQLxResult[A, R], *args: A) -> R:
    return {"id": 1, "name": "John Doe", "email": "john.doe@example.com"}


def query_optional(query: SQLxResult[A, R], *args: A) -> Optional[R]:
    return None


def query_many(query: SQLxResult[A, R], *args: A) -> list[R]:
    return []
