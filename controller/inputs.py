import uuid
from datetime import date

from view import console as v

_TRUE = {"true", "t", "1", "yes", "y", "так", "т"}
_FALSE = {"false", "f", "0", "no", "n", "ні", "н"}


def parse(kind, text):
    try:
        if kind == "int":
            return int(text)
        if kind == "date":
            return date.fromisoformat(text)
        if kind == "uuid":
            return uuid.UUID(text)
        if kind == "bool":
            value = text.strip().lower()
            if value in _TRUE:
                return True
            if value in _FALSE:
                return False
            raise ValueError("не булеве значення")
    except ValueError:
        raise ValueError({
            "int": "потрібно ввести ціле число",
            "date": "дата має бути у форматі РРРР-ММ-ДД",
            "uuid": "некоректний UUID",
            "bool": "введіть true або false",
        }[kind])
    return text


def read_optional(label, kind="str"):
    text = v.ask(f"{label} (Enter - пропустити): ")
    return None if text == "" else parse(kind, text)


def read_positive_int(label, max_value=1_000_000):
    n = parse("int", v.ask(f"{label}: "))
    if not 1 <= n <= max_value:
        raise ValueError(f"число має бути від 1 до {max_value}")
    return n