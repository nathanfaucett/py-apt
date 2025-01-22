from types import NoneType, UnionType
from typing import (
    Literal,
    NotRequired,
    Type,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from apt.openapi.spec import (
    OpenAPI,
    OpenAPISchema,
    OpenAPISchemaObject,
    OpenAPISchemaArray,
    OpenAPISchemaOneOf,
)
from typing import Any


def get_or_create_schema(
    cls: Type, openapi: OpenAPI, types: dict[Type, str]
) -> OpenAPISchema:
    name = types.get(cls)
    if name is not None:
        return {"$ref": f"#/components/schemas/{name}"}
    elif cls is int:
        return {"type": "integer"}
    elif cls is float:
        return {"type": "number"}
    elif cls is str:
        return {"type": "string"}
    elif cls is bool:
        return {"type": "boolean"}
    elif cls is Any:
        return {}
    elif cls is NoneType:
        return {"nullable": True}
    elif get_origin(cls) is list:
        array_schema: OpenAPISchemaArray = {"type": "array"}
        list_type = get_args(cls)[0]
        if list_type is not Any:
            array_schema["items"] = get_or_create_schema(list_type, openapi, types)
        return array_schema
    elif get_origin(cls) is dict:
        object_schema: OpenAPISchemaObject = {
            "type": "object",
            "additionalProperties": True,
        }
        value_type = get_args(cls)[1]
        if value_type is not Any:
            object_schema["additionalProperties"] = get_or_create_schema(
                value_type, openapi, types
            )
        return object_schema
    elif isinstance(cls, UnionType) or get_origin(cls) is Union:
        return OpenAPISchemaOneOf(
            oneOf=[get_or_create_schema(item, openapi, types) for item in get_args(cls)]
        )
    elif get_origin(cls) is Literal:
        enum = list(get_args(cls))
        literal_type = type(enum[0]) if len(enum) > 0 else None
        if literal_type is int:
            return {"type": "integer", "enum": enum}
        elif literal_type is float:
            return {"type": "number", "enum": enum}
        elif literal_type is bool:
            return {"type": "boolean"}
        else:
            return {"type": "string", "enum": enum}
    else:
        name = internal_create_unque_name(cls, openapi, types)
        class_schema: OpenAPISchemaObject = {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        }
        openapi["components"]["schemas"][name] = class_schema

        for [key, item] in get_type_hints(cls).items():
            if item is NotRequired:
                class_schema["properties"][key] = get_or_create_schema(
                    item.__type__, openapi, types
                )
            else:
                class_schema["properties"][key] = get_or_create_schema(
                    item, openapi, types
                )
                class_schema["required"].append(key)
        return {"$ref": f"#/components/schemas/{name}"}


def internal_create_unque_name(
    cls: Type, openapi: OpenAPI, types: dict[Type, str]
) -> str:
    if "components" not in openapi:
        openapi["components"] = {}
    if "schemas" not in openapi["components"]:
        openapi["components"]["schemas"] = {}

    name = cls.__name__
    count = 0
    while name in openapi["components"]["schemas"]:
        name = f"{cls.__name__}{count}"
        count += 1

    types[cls] = name

    return name
