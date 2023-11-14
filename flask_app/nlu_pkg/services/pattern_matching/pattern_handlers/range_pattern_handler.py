from spacy.tokens import Doc, Span

from flask_app.nlu_pkg.services.pattern_matching.spacy_matchers.base_spacy_matcher import BaseSpacyMatcher
from flask_app.nlu_pkg.models.sensor_dto.requirement_range import RequirementRange
from flask_app.nlu_pkg.services.pattern_matching.pattern_handlers.pattern_handler import PatternHandler
from flask_app.nlu_pkg.services.pattern_matching.spacy_matchers.spacy_matcher import SpacyMatcher
from flask_app.nlu_pkg.services.utils.str_utils import parse_number


class RangePatternHandler(PatternHandler):
    def __init__(self,
                 pattern_rules: list[dict],
                 first_number_index: int = 0,
                 second_number_index: int = -1):
        super().__init__(pattern_rules)
        self._first_number_index = first_number_index
        self._second_number_index = second_number_index

    def compute_result(self, matcher: SpacyMatcher, tokens: Doc | Span) -> RequirementRange:
        first_match = next(iter(super().compute_result(matcher, tokens)), None)
        if first_match:
            # print("RANGE MATCH", first_match)
            return RequirementRange(
                parse_number(first_match[self._first_number_index].text),
                parse_number(first_match[self._second_number_index].text)
            )
