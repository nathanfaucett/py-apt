import json
from aiohttp.web import run_app, Response, Application
import aiohttp_cors
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


@endpoint(
    path="/openapi.json",
    method="GET",
)
async def openapi_json() -> Response:
    return Response(
        text=json.dumps(test_openapi, indent=2), content_type="application/json"
    )


def main():
    api_router = Router("/api")
    api_router.add(openapi_json)

    util_router = Router("/util")
    util_router.add(test_endpoint)

    api_router.add(util_router)

    api_router.into_openapi(openapi=test_openapi)

    app = Application()
    app.add_routes(api_router.into_routes())
    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*"
            )
        },
    )
    for route in list(app.router.routes()):
        cors.add(route)
    run_app(app)


if __name__ == "__main__":
    main()
