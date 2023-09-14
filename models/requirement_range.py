from models.requirement_param import RequirementParam


class RequirementRange(RequirementParam):
    def __init__(self, start_value: int = None, end_value: int = None):
        super().__init__(start_value)
        self._end_value = end_value if end_value is None else int(end_value)

    def get_end_value(self) -> int:
        return self._end_value

    def set_end_value(self, end_value: int):
        self._end_value = int(end_value)

    end_value = property(get_end_value, set_end_value)
