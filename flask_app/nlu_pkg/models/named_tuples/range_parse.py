from typing import NamedTuple

from flask_app.nlu_pkg.models.enums.parse_status import ParseStatus
from flask_app.nlu_pkg.models.sensor_dto.requirement_param import RequirementParam


class ParseResult(NamedTuple):
    requirement: RequirementParam | None
    parse_status: ParseStatus
