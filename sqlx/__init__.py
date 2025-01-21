from typing import Any

from .result import SQLxResult


def sqlx(raw_query: str) -> SQLxResult[tuple[()], Any]:
    return SQLxResult(raw_query, (), Any)
