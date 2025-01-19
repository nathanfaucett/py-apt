from typing import Dict, NotRequired, Type

from apt.openapi.spec import OpenAPISchema, OpenAPISchemaObject, OpenAPIFormat


def get_or_create_component(
    type: Type, components: Dict[str, OpenAPISchema]
) -> OpenAPISchema:
    if is_primitive_schema(type):
        return type_to_schema(type)
    name = type.__name__
    if name in components:
        return components[name]
    schema = type_to_schema(type)
    components[name] = schema
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
