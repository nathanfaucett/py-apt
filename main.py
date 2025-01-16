from aiohttp.web import run_app, Response, Application
from msgspec import Struct

from apt.extract.json import JSON
from apt.extract.query import Query
from apt.router import method, path
from apt.router.router import Router


class User(Struct):
    name: str


class LimitAndOffsetQuery(Struct):
    limit: int | None = None
    offset: int | None = None


@method("POST")
@path("/echo")
async def echo(
    user_json: JSON[User], limit_and_offset_query: Query[LimitAndOffsetQuery]
) -> Response:
    user = user_json.get()
    print(user)
    limit_and_offset = limit_and_offset_query.get()
    print(limit_and_offset)
    return Response(text="Hello, " + user.name)


def main():
    router = Router()
    router.add(echo)

    app = Application()
    app.add_routes(router.into_routes())
    run_app(app)


if __name__ == "__main__":
    main()
