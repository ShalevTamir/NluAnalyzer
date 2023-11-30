from flask_app.nlu_pkg.models.enums.duration_type import DurationType
from flask_app.nlu_pkg.models.sensor_dto.requirement_param import RequirementParam


class Duration:
    def __init__(self, duration_type: DurationType, requirement_param: RequirementParam | None):
        self.duration_type = duration_type
        self.requirement_param = requirement_param
