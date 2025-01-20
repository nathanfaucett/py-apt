from typing import Literal, TypedDict

from apt.sql.query import QueryResult

class User(TypedDict):
    id: int
    name: str
    email: str

def sql(query: Literal["select * from users;"]) -> QueryResult[User]: ...
