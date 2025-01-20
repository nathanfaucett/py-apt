from typing import TypeVar

from apt.sql.query import QueryResult


T = TypeVar("T")


def query_one(query: QueryResult[T]) -> T:
    return {}
