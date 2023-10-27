from typing import NamedTuple

from models.enums.parse_status import ParseStatus
from models.sensor_dto.requirement_param import RequirementParam


class ParseResult(NamedTuple):
    requirement: RequirementParam | None
    parse_status: ParseStatus
