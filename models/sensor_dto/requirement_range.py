from models.sensor_dto.requirement_param import RequirementParam


class RequirementRange(RequirementParam):
    def __init__(self, start_value: int | float = None, end_value: int | float = None):
        super().__init__(start_value)
        self._end_value = end_value if end_value is None else super()._parse_value(end_value)

    def get_end_value(self) -> int | float:
        return self._end_value

    def set_end_value(self, end_value: int | float):
        self._end_value = super()._parse_value(end_value)

    end_value = property(get_end_value, set_end_value)
