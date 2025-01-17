from typing import Any


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
