from typing import NamedTuple

from ..enums.parse_status import ParseStatus
from ..sensor_dto.requirement_param import RequirementParam


class ParseResult(NamedTuple):
    requirement: list[RequirementParam]
    parse_status: ParseStatus
