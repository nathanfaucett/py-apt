from pprint import pprint
from aiohttp.web import run_app, Response, Application
from msgspec import Struct

from apt.extract import JSON, Query, Path
from apt.openapi import openapi, OpenAPIInfo
from apt.router import endpoint, Router
from sqlx import sqlx

from db import query_one


test_openapi = openapi(
    info=OpenAPIInfo(
        title="Test API",
        version="1.0.0",
        description="A test API",
    ),
)


class NewUserRequest(Struct):
    name: str


class LimitAndOffsetQuery(Struct):
    limit: int | None = None
    offset: int | None = None


@endpoint(
    path="/{action}/{id}",
    method="POST",
    responses={
        200: ("text/plain", str),
        400: {
            "content_type": "text/plain",
            "items": str,
            "format": "error",
            "min_items": 1,
        },
    },
)
async def test_endpoint(
    new_user_json: JSON[NewUserRequest],
    limit_and_offset_query: Query[LimitAndOffsetQuery],
    path: Path[tuple[str, int]],
) -> Response:
    new_user = new_user_json.get()
    print(new_user)

    limit_and_offset = limit_and_offset_query.get()
    print(limit_and_offset)

    (action, path_id) = path.get()
    print(action, path_id)

    user = query_one(sqlx("select * from users where id = $1;"), path_id)
    print(user)

    return Response(text="Hello, " + new_user.name)


def main():
    api_router = Router("/api")

    util_router = Router("/util")
    util_router.add(test_endpoint)

    api_router.add(util_router)

    api_router.into_openapi(openapi=test_openapi)
    pprint(test_openapi)

    app = Application()
    app.add_routes(api_router.into_routes())
    run_app(app)


if __name__ == "__main__":
    main()
