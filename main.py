import json
from typing import Optional
from aiohttp import BodyPartReader
from aiohttp.web import run_app, Response, Application
import aiohttp_cors
from pydantic import BaseModel

from apt.extract import JSON, Query, Path
from apt.extract.multipart import Multipart
from apt.openapi import openapi, OpenAPIInfo
from apt.openapi.spec import OpenAPI, OpenAPIBinaryFormat
from apt.router import endpoint, Router


test_openapi = openapi(
    info=OpenAPIInfo(
        title="Test API",
        version="1.0.0",
        description="A test API",
    ),
)


class NewUserRequest(BaseModel):
    name: str


class User(BaseModel):
    id: int
    name: str


class LimitAndOffsetQuery(BaseModel):
    limit: Optional[int] = None
    offset: Optional[int] = None


@endpoint(
    path="/{action}/{id}",
    method="POST",
    responses={
        200: ("application/json", User),
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

    user = User(id=1, name=new_user.name)

    return Response(body=user.model_dump_json(), content_type="application/json")


class MultipartUpload:
    bytes: bytes
    string: OpenAPIBinaryFormat


@endpoint(
    path="/upload",
    method="POST",
    responses={204: None},
)
async def multipart_endpoint(multipart: Multipart[MultipartUpload]) -> Response:
    upload = multipart.get()
    print("bytes", upload.bytes)
    print("string", upload.string)
    return Response(status=204)


@endpoint(
    path="/openapi.json",
    method="GET",
    responses={200: ("application/json", OpenAPI)},
)
async def openapi_json() -> Response:
    return Response(body=json.dumps(test_openapi), content_type="application/json")


def main():
    api_router = Router("/api")
    api_router.add(openapi_json)

    util_router = Router("/util")
    util_router.add(test_endpoint)

    util_router.add(multipart_endpoint)

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
