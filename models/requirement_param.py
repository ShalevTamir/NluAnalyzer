class RequirementParam:
    def __init__(self, value: int = None):
        self._value = value if value is None else int(value)

    def get_value(self) -> int:
        return self._value

    def set_value(self, start_value: int):
        self._value = int(start_value)

    value = property(get_value, set_value)
