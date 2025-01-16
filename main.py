from aiohttp.web import run_app, post, Response, Application

from apt.extract.json import JSON
from apt.router import method, path
from apt.router.handler import Handler

from msgspec import Struct


class User(Struct):
    name: str


@method("POST")
@path("/echo")
async def echo(user_json: JSON[User]) -> Response:
    user = user_json.get()
    return Response(text="Hello, " + user.name)


def main():
    app = Application()

    handler = Handler(echo)
    handle = handler.into_handle()

    app.add_routes([post(handler.path(), handle)])

    run_app(app)


if __name__ == "__main__":
    main()
