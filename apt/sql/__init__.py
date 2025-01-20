from typing import Any, TypeVar

from apt.sql.query import QueryResult


def sql(raw_query: str) -> QueryResult[Any]:
    return QueryResult(raw_query, Any)
