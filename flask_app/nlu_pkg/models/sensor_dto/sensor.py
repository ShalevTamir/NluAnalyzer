from flask_app.nlu_pkg.models.sensor_dto.duration import Duration
from flask_app.nlu_pkg.models.sensor_dto.requirement_param import RequirementParam


class Sensor:
    def __init__(self, parameter_name: str, requirement_param: RequirementParam, duration: Duration):
        self.parameter_name = parameter_name
        self.requirement_param = requirement_param
        self.duration = duration
