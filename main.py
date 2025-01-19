from pprint import pprint
from aiohttp.web import run_app, Response, Application
from msgspec import Struct

from apt.extract import JSON, Query
from apt.router import endpoint, Router, Handler


class NewUserRequest(Struct):
    name: str


class LimitAndOffsetQuery(Struct):
    limit: int | None = None
    offset: int | None = None


@endpoint(
    path="/echo",
    method="POST",
    request_body=("application/json", NewUserRequest),
    responses={200: ("text/plain", str), 400: ("text/plain", str)},
)
async def echo(
    new_user_json: JSON[NewUserRequest],
    limit_and_offset_query: Query[LimitAndOffsetQuery],
) -> Response:
    new_user = new_user_json.get()
    print(new_user)
    limit_and_offset = limit_and_offset_query.get()
    print(limit_and_offset)
    return Response(text="Hello, " + new_user.name)


def main():
    api_router = Router("/api")

    util_router = Router("/util")
    util_router.add(echo)

    api_router.add(util_router)

    openapi_components = {}
    openapi_paths = api_router.into_openapi(components=openapi_components)
    pprint(openapi_components)
    pprint(openapi_paths)

    app = Application()
    app.add_routes(api_router.into_routes())
    run_app(app)


if __name__ == "__main__":
    main()
