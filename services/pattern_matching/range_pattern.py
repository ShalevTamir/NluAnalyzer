from typing import Callable

from spacy.matcher import Matcher
from spacy.tokens import Doc, Span, Token

from models.sensor_dto.requirement_range import RequirementRange
from services.pattern_matching.pattern import Pattern
from services.utils.str_utils import parse_number


class RangePattern(Pattern):
    def __init__(self,
                 pattern_rules: list[dict],
                 first_number_index: int = 0,
                 second_number_index: int = -1):
        super().__init__(pattern_rules)
        self._first_number_index = first_number_index
        self._second_number_index = second_number_index

    def compute_result(self, matcher: Matcher, tokens: Doc | Span):
        match = super().compute_result(matcher, tokens)
        if match:
            return RequirementRange(
                parse_number(match[self._first_number_index].text),
                parse_number(match[self._second_number_index].text)
            )

