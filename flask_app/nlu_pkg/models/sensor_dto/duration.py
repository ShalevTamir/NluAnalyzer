from ..enums.duration_type import DurationType
from .requirement_param import RequirementParam


class Duration:
    def __init__(self, duration_type: DurationType, requirement_param: RequirementParam | None):
        self.duration_type = duration_type
        self.requirement_param = requirement_param
