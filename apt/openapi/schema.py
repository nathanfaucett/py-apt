from typing import (
    NotRequired,
    Type,
    get_args,
    get_type_hints,
)

from apt.openapi.spec import OpenAPI, OpenAPISchema, OpenAPISchemaObject


def get_or_create_component(
    cls: Type, openapi: OpenAPI, types: dict[Type, str]
) -> OpenAPISchema:
    if is_primitive_schema(cls):
        return type_to_schema(cls)

    name = types.get(cls)
    if name is None:
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

        schema = type_to_schema(cls)
        openapi["components"]["schemas"][name] = schema

    return {"$ref": f"#components/schemas/{name}"}


def is_primitive_schema(
    cls: Type,
) -> bool:
    if cls is int:
        return True
    elif cls is float:
        return True
    elif cls is str:
        return True
    elif cls is bool:
        return True
    elif cls is list:
        return True
    elif cls is dict:
        return True
    else:
        return False


def type_to_schema(cls: Type) -> OpenAPISchema:
    if cls is int:
        return {"type": "integer"}
    elif cls is float:
        return {"type": "number"}
    elif cls is str:
        return {"type": "string"}
    elif cls is bool:
        return {"type": "boolean"}
    elif cls is list:
        return {"type": "array"}
    elif cls is dict:
        return {"type": "object", "additionalProperties": True}
    else:
        schema: OpenAPISchemaObject = {
            "type": "object",
            "properties": {},
            "required": [],
        }
        for [key, item] in get_type_hints(cls).items():
            item_schema: OpenAPISchema
            if item is NotRequired:
                item_schema = type_to_schema(item.__type__)
            else:
                (item_types, is_nonable) = extract_types(item)
                if len(item_types) == 1:
                    item_schema = type_to_schema(item_types[0])
                elif len(item_types) > 1:
                    item_schema = {"oneOf": [type_to_schema(v) for v in item_types]}
                else:
                    item_schema = type_to_schema(item)
                if is_nonable:
                    schema["required"].append(key)
            schema["properties"][key] = item_schema
        return schema


def extract_types(cls: Type) -> tuple[list[Type], bool]:
    types = []
    is_nonable = False
    for value in get_args(cls):
        if value is type(None):
            is_nonable = True
            continue
        types.append(value)
    return (types, is_nonable)
