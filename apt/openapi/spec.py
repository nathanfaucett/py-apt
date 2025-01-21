from typing import Any, Literal, NotRequired, TypedDict, Union


OpenAPIIn = Literal["path", "query", "header"]
OpenAPIStringFormat = Union[
    Literal["data", "date-time", "password", "byte", "binary"],
    str,
]
OpenAPINumberFormat = Literal["float", "double", "int32", "int64"]
OpenAPIFormat = Union[OpenAPIStringFormat, OpenAPINumberFormat]
OpenAPIMethod = Literal[
    "get", "head", "options", "post", "put", "patch", "delete", "trace"
]


class OpenAPISchemaBase(TypedDict):
    nullable: NotRequired[bool]
    example: NotRequired[Any]
    description: NotRequired[str]
    readOnly: NotRequired[bool]
    writeOnly: NotRequired[bool]
    deprecated: NotRequired[bool]


OpenAPISchemaRef = TypedDict(
    "OpenAPISchemaRef",
    {
        "nullable": NotRequired[bool],
        "example": NotRequired[Any],
        "description": NotRequired[str],
        "readOnly": NotRequired[bool],
        "writeOnly": NotRequired[bool],
        "deprecated": NotRequired[bool],
        "$ref": str,
    },
)


class OpenAPISchemaAnyValue(OpenAPISchemaBase):
    pass


class OpenAPISchemaDiscriminator(TypedDict):
    propertyName: str
    mapping: NotRequired[dict[str, str]]


class OpenAPISchemaOneOf(OpenAPISchemaBase):
    oneOf: list["OpenAPISchema"]
    discriminator: NotRequired[OpenAPISchemaDiscriminator]


class OpenAPISchemaAllOf(OpenAPISchemaBase):
    allOf: list["OpenAPISchema"]


class OpenAPISchemaAnyOf(OpenAPISchemaBase):
    anyOf: list["OpenAPISchema"]


OpenAPISchemaNot = TypedDict(
    "OpenAPISchemaNot",
    {
        "nullable": NotRequired[bool],
        "example": NotRequired[Any],
        "description": NotRequired[str],
        "readOnly": NotRequired[bool],
        "writeOnly": NotRequired[bool],
        "deprecated": NotRequired[bool],
        "not": list["OpenAPISchema"],
    },
)


class OpenAPISchemaBoolean(OpenAPISchemaBase):
    type: Literal["boolean"]


class OpenAPISchemaString(OpenAPISchemaBase):
    type: Literal["string"]
    format: NotRequired[OpenAPIStringFormat]
    enum: NotRequired[list[str]]
    default: NotRequired[str]
    pattern: NotRequired[str]
    minLength: NotRequired[int]
    maxLength: NotRequired[int]


class OpenAPISchemaNumber(OpenAPISchemaBase):
    type: Literal["number"]
    format: NotRequired[OpenAPINumberFormat]
    enum: NotRequired[list[str]]
    default: NotRequired[str]
    minimum: NotRequired[Union[int, float]]
    exclusiveMinimum: NotRequired[bool]
    maximum: NotRequired[Union[int, float]]
    exclusiveMaximum: NotRequired[bool]
    multipleOf: NotRequired[Union[int, float]]


class OpenAPISchemaInteger(OpenAPISchemaBase):
    type: Literal["integer"]
    format: NotRequired[OpenAPINumberFormat]
    enum: NotRequired[list[str]]
    default: NotRequired[str]
    minimum: NotRequired[Union[int, float]]
    exclusiveMinimum: NotRequired[bool]
    maximum: NotRequired[Union[int, float]]
    exclusiveMaximum: NotRequired[bool]
    multipleOf: NotRequired[Union[int, float]]


class OpenAPISchemaArray(OpenAPISchemaBase):
    type: Literal["array"]
    items: NotRequired["OpenAPISchema"]
    minItems: NotRequired[int]
    maxItems: NotRequired[int]
    uniqueItems: NotRequired[bool]


class OpenAPISchemaObject(OpenAPISchemaBase):
    type: Literal["object"]
    properties: NotRequired[dict[str, "OpenAPISchema"]]
    additionalProperties: NotRequired[Union["OpenAPISchema", bool]]
    required: NotRequired[list[str]]
    minProperties: NotRequired[int]
    maxProperties: NotRequired[int]


OpenAPISchema = Union[
    OpenAPISchemaRef,
    OpenAPISchemaString,
    OpenAPISchemaInteger,
    OpenAPISchemaNumber,
    OpenAPISchemaBoolean,
    OpenAPISchemaArray,
    OpenAPISchemaObject,
    OpenAPISchemaAnyValue,
    OpenAPISchemaOneOf,
    OpenAPISchemaAllOf,
    OpenAPISchemaAnyOf,
    OpenAPISchemaNot,
]


OpenAPIParameter = TypedDict(
    "OpenAPIParameter",
    {
        "name": str,
        "in": OpenAPIIn,
        "description": NotRequired[str],
        "required": NotRequired[Literal[True]],
        "schema": NotRequired[OpenAPISchema],
    },
)


class OpenAPIBodyContent(TypedDict):
    schema: NotRequired[OpenAPISchema]


class OpenAPIBody(TypedDict):
    description: NotRequired[str]
    required: NotRequired[Literal[True]]
    content: dict[str, OpenAPIBodyContent]


class OpenAPIExternalDocs(TypedDict):
    url: str
    description: NotRequired[str]


class OpenAPIRoute(TypedDict):
    tags: NotRequired[list[str]]
    summary: NotRequired[str]
    description: NotRequired[str]
    operationId: NotRequired[str]
    security: NotRequired[list[dict[str, list[str]]]]
    parameters: NotRequired[list[OpenAPIParameter]]
    requestBody: NotRequired[OpenAPIBody]
    responses: NotRequired[dict[int, OpenAPIBody]]
    externalDocs: NotRequired[OpenAPIExternalDocs]


class OpenAPIPath(TypedDict):
    description: NotRequired[str]
    servers: NotRequired[list[dict[str, "OpenAPIServer"]]]
    get: NotRequired[OpenAPIRoute]
    head: NotRequired[OpenAPIRoute]
    post: NotRequired[OpenAPIRoute]
    patch: NotRequired[OpenAPIRoute]
    put: NotRequired[OpenAPIRoute]
    delete: NotRequired[OpenAPIRoute]
    options: NotRequired[OpenAPIRoute]
    trace: NotRequired[OpenAPIRoute]


OpenAPISecuritySchemaBase = TypedDict(
    "OpenAPISecuritySchemaBase",
    {
        "name": NotRequired[str],
        "description": NotRequired[str],
        "in": NotRequired[OpenAPIIn],
    },
)


class OpenAPISecuritySchemaHTTP(OpenAPISecuritySchemaBase):
    type: Literal["http"]
    scheme: Literal[
        "basic",
        "bearer",
    ]


class OpenAPISecuritySchemaAPIKey(OpenAPISecuritySchemaBase):
    type: Literal["apiKey"]


class OpenAPISecuritySchemaOAuth2(OpenAPISecuritySchemaBase):
    type: Literal["oauth2"]
    flows: NotRequired[dict[str, dict[str, Any]]]


class OpenAPISecuritySchemaOpenIdConnect(OpenAPISecuritySchemaBase):
    type: Literal["openIdConnect"]
    openIdConnectUrl: NotRequired[str]


OpenAPISecuritySchema = Union[
    OpenAPISecuritySchemaHTTP,
    OpenAPISecuritySchemaAPIKey,
    OpenAPISecuritySchemaOAuth2,
    OpenAPISecuritySchemaOpenIdConnect,
]


class OpenAPIComponents(TypedDict):
    schemas: NotRequired[dict[str, OpenAPISchema]]
    securitySchemes: NotRequired[dict[str, OpenAPISecuritySchema]]


class OpenAPIInfoContact(TypedDict):
    name: NotRequired[str]
    url: NotRequired[str]
    email: NotRequired[str]


class OpenAPIInfoLicense(TypedDict):
    name: NotRequired[str]
    url: NotRequired[str]


class OpenAPIInfo(TypedDict):
    title: NotRequired[str]
    version: NotRequired[str]
    description: NotRequired[str]
    termsOfService: NotRequired[str]
    contact: NotRequired[dict[str, Union[str, OpenAPIInfoContact]]]
    license: NotRequired[Union[str, OpenAPIInfoLicense, dict[str, OpenAPIInfoLicense]]]


class OpenAPIServer(TypedDict):
    url: str
    description: NotRequired[str]
    variables: NotRequired[dict[str, dict[str, OpenAPISchema]]]


class OpenAPITag(TypedDict):
    name: str
    description: NotRequired[str]
    externalDocs: NotRequired[OpenAPIExternalDocs]


class OpenAPI(TypedDict):
    openapi: NotRequired[str]
    info: NotRequired[OpenAPIInfo]
    servers: NotRequired[list[dict[str, OpenAPIServer]]]
    security: NotRequired[list[dict[str, list[str]]]]
    tags: NotRequired[list[OpenAPITag]]
    paths: NotRequired[dict[str, OpenAPIPath]]
    components: NotRequired[OpenAPIComponents]
    externalDocs: NotRequired[OpenAPIExternalDocs]
