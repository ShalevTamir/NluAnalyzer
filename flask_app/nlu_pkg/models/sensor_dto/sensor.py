from .duration import Duration
from .requirement_param import RequirementParam


class Sensor:
    def __init__(self, parameter_name: str, requirement_param: RequirementParam, duration: Duration = None):
        self.parameter_name = parameter_name
        self.requirement_param = requirement_param
        if duration:
            self.duration = duration
