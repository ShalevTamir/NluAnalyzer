from services.utils.general import is_castable


class RequirementParam:
    def __init__(self, value: int | float = None):
        self._value = value if value is None else self._parse_value(value)

    def get_value(self) -> int | float:
        return self._value

    def set_value(self, start_value: int | float):
        self._value = self._parse_value(start_value)

    def _parse_value(self, value: int | float) -> int | float:
        if isinstance(value, int) or issubclass(value.__class__, int) or is_castable(value, int):
            return int(value)
        else:
            return float(value)

    value = property(get_value, set_value)
