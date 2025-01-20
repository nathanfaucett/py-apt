from pprint import pprint
from aiohttp.web import run_app, Response, Application
from msgspec import Struct

from apt.extract import JSON, Query, Path
from apt.openapi import openapi
from apt.openapi.spec import OpenAPIInfo
from apt.router import endpoint, Router
from apt.sql import sql

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
    request_body=("application/json", NewUserRequest),
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
    (action, id) = path.get()
    print(action, id)
    return Response(text="Hello, " + new_user.name)


def main():
    users = query_one(sql("select * from users;"))
    print(users)

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
