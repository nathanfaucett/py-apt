from types import NoneType, UnionType
from typing import (
    Literal,
    NotRequired,
    Type,
    TypeAliasType,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from aiohttp import BodyPartReader

from apt.openapi.spec import (
    OpenAPI,
    OpenAPIBinaryFormat,
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
    elif cls is bytes or cls is BodyPartReader or cls is OpenAPIBinaryFormat:
        return {"type": "string", "format": "binary"}
    elif cls is Any:
        return {}
    elif cls is NoneType:
        return {"nullable": True}
    cls_origin = get_origin(cls)
    if cls_origin is list:
        array_schema = OpenAPISchemaArray(type="array")
        list_type = get_args(cls)[0]
        if list_type is not Any:
            array_schema["items"] = get_or_create_schema(list_type, openapi, types)
        return array_schema
    elif cls_origin is dict:
        object_schema = OpenAPISchemaObject(
            type="object",
            additionalProperties=True,
        )
        value_type = get_args(cls)[1]
        if value_type is not Any:
            object_schema["additionalProperties"] = get_or_create_schema(
                value_type, openapi, types
            )
        return object_schema
    elif cls_origin is Union or isinstance(cls, UnionType):
        return OpenAPISchemaOneOf(
            oneOf=[get_or_create_schema(item, openapi, types) for item in get_args(cls)]
        )
    elif cls_origin is Literal:
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
    elif isinstance(cls, TypeAliasType):
        name = internal_create_unique_name(cls, cls.__name__, openapi, types)
        openapi["components"]["schemas"][name] = get_or_create_schema(
            cls.__value__, openapi, types
        )
        return {"$ref": f"#/components/schemas/{name}"}
    else:
        name = internal_create_unique_name(cls, cls.__name__, openapi, types)
        class_schema = OpenAPISchemaObject(
            type="object",
            properties={},
            required=[],
            additionalProperties=False,
        )
        openapi["components"]["schemas"][name] = class_schema

        for [key, item_cls] in get_type_hints(cls).items():
            item_schema: OpenAPISchema
            item_required = False
            if item_cls is NotRequired:
                item_schema = get_or_create_schema(item_cls.__type__, openapi, types)
            elif isinstance(item_cls, UnionType) or get_origin(item_cls) is Union:
                item_cls_args = [
                    item_cls_arg
                    for item_cls_arg in get_args(item_cls)
                    if item_cls_arg is not NoneType
                ]
                if len(item_cls_args) == 1:
                    item_schema = get_or_create_schema(item_cls_args[0], openapi, types)
                else:
                    item_schema = OpenAPISchemaOneOf(
                        oneOf=[
                            get_or_create_schema(item_clss_arg, openapi, types)
                            for item_clss_arg in item_cls_args
                        ]
                    )
            else:
                item_schema = get_or_create_schema(item_cls, openapi, types)
                item_required = True
            class_schema["properties"][key] = item_schema
            if item_required:
                class_schema["required"].append(key)
        return {"$ref": f"#/components/schemas/{name}"}


def internal_create_unique_name(
    cls: Type, name: str, openapi: OpenAPI, types: dict[Type, str]
) -> str:
    if "components" not in openapi:
        openapi["components"] = {}
    if "schemas" not in openapi["components"]:
        openapi["components"]["schemas"] = {}

    new_name = name
    count = 0
    while new_name in openapi["components"]["schemas"]:
        new_name = f"{name}{count}"
        count += 1

    types[cls] = new_name

    return new_name
