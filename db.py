from typing import TypeVar

from sqlx.result import SQLxResult


A = TypeVar("A")
R = TypeVar("R")


def query_one(query: SQLxResult[A, R], *args: A) -> R:
    print(query, *args)
    return {"id": 1, "name": "John Doe", "email": "john.doe@example.com"}
