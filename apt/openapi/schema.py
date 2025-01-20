from typing import NotRequired, Dict, Type

from apt.openapi.spec import OpenAPI, OpenAPISchema, OpenAPISchemaObject


def get_or_create_component(
    cls: Type, openapi: OpenAPI, types: Dict[Type, str]
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
        for [key, value] in cls.__annotations__.items():
            if value is NotRequired:
                value_schema = type_to_schema(value.__type__)
            else:
                value_schema = type_to_schema(value)
                schema["required"].append(key)
            schema["properties"][key] = value_schema
        return schema
