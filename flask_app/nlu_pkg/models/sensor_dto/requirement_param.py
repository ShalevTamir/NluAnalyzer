class RequirementParam:
    def __init__(self, value: int | float = None):
        self.value = value if value is None else self._parse_value(value)

    def _parse_value(self, value: int | float) -> int | float:

        if isinstance(value, int):
            return int(value)
        else:
            return float(value)

