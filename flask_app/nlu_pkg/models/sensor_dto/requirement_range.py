from flask_app.nlu_pkg.models.sensor_dto.requirement_param import RequirementParam


class RequirementRange(RequirementParam):
    def __init__(self, start_value: int | float = None, end_value: int | float = None):
        super().__init__(start_value)
        self.end_value = end_value if end_value is None else super()._parse_value(end_value)
