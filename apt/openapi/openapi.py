from typing import Dict, List
from apt.openapi.spec import (
    OpenAPI,
    OpenAPIComponents,
    OpenAPIExternalDocs,
    OpenAPIInfo,
    OpenAPIPath,
    OpenAPIServer,
    OpenAPITag,
)


def openapi(
    info: OpenAPIInfo | None = None,
    servers: List[Dict[str, OpenAPIServer]] | None = None,
    security: List[Dict[str, List[str]]] | None = None,
    tags: List[OpenAPITag] | None = None,
    paths: Dict[str, OpenAPIPath] | None = None,
    components: OpenAPIComponents | None = None,
    external_docs: OpenAPIExternalDocs | None = None,
) -> OpenAPI:
    spec: OpenAPI = {"openapi": "3.0.3"}
    if info is not None:
        spec["info"] = info
    if servers is not None:
        spec["servers"] = servers
    if security is not None:
        spec["security"] = security
    if tags is not None:
        spec["tags"] = tags
    if paths is not None:
        spec["paths"] = paths
    if components is not None:
        spec["components"] = components
    if external_docs is not None:
        spec["externalDocs"] = external_docs
    return spec
