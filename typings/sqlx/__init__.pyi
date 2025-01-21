from typing import Literal, TypedDict

from sqlx.result import SQLxResult

class User(TypedDict):
    id: int
    name: str
    email: str

def sqlx(
    query: Literal["select * from users where id = $1;"],
) -> SQLxResult[tuple[int], User]: ...
