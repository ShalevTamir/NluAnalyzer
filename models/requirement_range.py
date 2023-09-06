from models.requirement_param import RequirementParam


class RequirementRange(RequirementParam):
    def __init__(self, start_value, end_value):
        super().__init__(start_value)
        self.end_value = end_value
