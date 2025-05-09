from typing import Any, Dict, Optional


truthy_values = ["true", "yes", "y", "on"]
falsey_values = ["false", "no", "n", "off"]


def str_to_python_value(element: str) -> Any:
    number_value = parse_number(element)
    if number_value is not None:
        return number_value
    element_lower = element.lower()
    if element_lower in truthy_values:
        return True
    if element_lower in falsey_values:
        return False
    return element


def parse_number(element: str | None) -> float | int | None:
    if element is None:
        return None
    if element.isnumeric():
        return int(element)
    return try_float(element)


def try_int(element: Any) -> int | None:
    if element is None:
        return None
    try:
        return int(element)
    except ValueError:
        return None


def try_float(element: Any) -> float | None:
    if element is None:
        return None
    try:
        return float(element)
    except ValueError:
        return None


def to_camel_case(text: str) -> str:
    words = text.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


def dict_from_form_data(data: Optional[str]) -> Dict[str, str]:
    result: Dict[str, str] = {}
    if not data:
        return result
    parts = data.split(";")
    for part in parts:
        part = part.strip()
        if part == "form-data":
            continue
        key, value = part.split("=", 2)
        key = key.strip().lower()
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        result[key] = str_to_python_value(value)
    return result
