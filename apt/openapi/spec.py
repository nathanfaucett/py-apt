from typing import Any, Dict, List, Literal, NotRequired, TypedDict, Union


OpenAPIIn = Literal["path", "query", "header"]
OpenAPIStringFormat = Union[
    Literal["data", "date-time", "password", "byte", "binary"],
    str,
]
OpenAPINumberFormat = Literal["float", "double", "int32", "int64"]


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
    mapping: NotRequired[Dict[str, str]]


class OpenAPISchemaOneOf(OpenAPISchemaBase):
    oneOf: List["OpenAPISchema"]
    discriminator: NotRequired[OpenAPISchemaDiscriminator]


class OpenAPISchemaAllOf(OpenAPISchemaBase):
    allOf: List["OpenAPISchema"]


class OpenAPISchemaAnyOf(OpenAPISchemaBase):
    anyOf: List["OpenAPISchema"]


OpenAPISchemaNot = TypedDict(
    "OpenAPISchemaNot",
    {
        "nullable": NotRequired[bool],
        "example": NotRequired[Any],
        "description": NotRequired[str],
        "readOnly": NotRequired[bool],
        "writeOnly": NotRequired[bool],
        "deprecated": NotRequired[bool],
        "not": List["OpenAPISchema"],
    },
)


class OpenAPISchemaBoolean(OpenAPISchemaBase):
    type: Literal["boolean"]


class OpenAPISchemaString(OpenAPISchemaBase):
    type: Literal["string"]
    format: NotRequired[OpenAPIStringFormat]
    enum: NotRequired[List[str]]
    default: NotRequired[str]
    pattern: NotRequired[str]
    minLength: NotRequired[int]
    maxLength: NotRequired[int]


class OpenAPISchemaNumber(OpenAPISchemaBase):
    type: Literal["number"]
    format: NotRequired[OpenAPINumberFormat]
    enum: NotRequired[List[str]]
    default: NotRequired[str]
    minimum: NotRequired[Union[int, float]]
    exclusiveMinimum: NotRequired[bool]
    maximum: NotRequired[Union[int, float]]
    exclusiveMaximum: NotRequired[bool]
    multipleOf: NotRequired[Union[int, float]]


class OpenAPISchemaInteger(OpenAPISchemaBase):
    type: Literal["integer"]
    format: NotRequired[OpenAPINumberFormat]
    enum: NotRequired[List[str]]
    default: NotRequired[str]
    minimum: NotRequired[Union[int, float]]
    exclusiveMinimum: NotRequired[bool]
    maximum: NotRequired[Union[int, float]]
    exclusiveMaximum: NotRequired[bool]
    multipleOf: NotRequired[Union[int, float]]


class OpenAPISchemaArray(OpenAPISchemaBase):
    type: Literal["array"]
    items: NotRequired[List["OpenAPISchema"]]
    minItems: NotRequired[int]
    maxItems: NotRequired[int]
    uniqueItems: NotRequired[bool]


class OpenAPISchemaObject(OpenAPISchemaBase):
    type: Literal["object"]
    properties: NotRequired[Dict[str, "OpenAPISchema"]]
    additionalProperties: NotRequired[Union["OpenAPISchema", bool]]
    required: NotRequired[List[str]]
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
    content: Dict[str, OpenAPIBodyContent]


class OpenAPIExternalDocs(TypedDict):
    url: str
    description: NotRequired[str]


class OpenAPIRoute(TypedDict):
    tags: NotRequired[List[str]]
    summary: NotRequired[str]
    description: NotRequired[str]
    operationId: NotRequired[str]
    security: NotRequired[List[Dict[str, List[str]]]]
    parameters: NotRequired[List[OpenAPIParameter]]
    requestBody: NotRequired[OpenAPIBody]
    responses: NotRequired[Dict[int, OpenAPIBody]]
    externalDocs: NotRequired[OpenAPIExternalDocs]


class OpenAPIPath(TypedDict):
    description: NotRequired[str]
    servers: NotRequired[List[Dict[str, "OpenAPIServer"]]]
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
    flows: NotRequired[Dict[str, Dict[str, Any]]]


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
    schemas: NotRequired[Dict[str, OpenAPISchema]]
    securitySchemes: NotRequired[Dict[str, OpenAPISecuritySchema]]


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
    contact: NotRequired[Dict[str, Union[str, OpenAPIInfoContact]]]
    license: NotRequired[Union[str, OpenAPIInfoLicense, Dict[str, OpenAPIInfoLicense]]]


class OpenAPIServer(TypedDict):
    url: str
    description: NotRequired[str]
    variables: NotRequired[Dict[str, Dict[str, OpenAPISchema]]]


class OpenAPITag(TypedDict):
    name: str
    description: NotRequired[str]
    externalDocs: NotRequired[OpenAPIExternalDocs]


class OpenAPI(TypedDict):
    openapi: NotRequired[str]
    info: NotRequired[OpenAPIInfo]
    servers: NotRequired[List[Dict[str, OpenAPIServer]]]
    security: NotRequired[List[Dict[str, List[str]]]]
    tags: NotRequired[List[OpenAPITag]]
    paths: NotRequired[Dict[str, OpenAPIPath]]
    components: NotRequired[OpenAPIComponents]
    externalDocs: NotRequired[OpenAPIExternalDocs]
