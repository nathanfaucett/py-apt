from aiohttp.web import run_app, post, Response, Application

from apt.extract.json import JSON
from apt.router import method, path
from apt.router.handler import Handler

from msgspec import Struct

from apt.router.router import Router


class User(Struct):
    name: str


@method("POST")
@path("/echo")
async def echo(user_json: JSON[User]) -> Response:
    user = user_json.get()
    return Response(text="Hello, " + user.name)


def main():
    router = Router()
    router.add(echo)

    app = Application()
    app.add_routes(router.into_routes())
    run_app(app)


if __name__ == "__main__":
    main()
