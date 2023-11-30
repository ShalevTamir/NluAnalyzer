# import logging
from spacy.tokens import Span, Doc

from flask_app.nlu_pkg.models.definitions.spacy_def import SPACY_MODEL, SPACY_POS_ATTR, NUMERICAL_POS_TAG
from flask_app.nlu_pkg.models.enums.relation_group import RelationGroup
from flask_app.nlu_pkg.models.named_tuples.range_parse import ParseResult
from flask_app.nlu_pkg.models.named_tuples.relational_bound import RelationalBound
from flask_app.nlu_pkg.models.pattern_groups.range_patterns_group import RangePatternsGroup
from flask_app.nlu_pkg.models.sensor_dto.requirement_range import RequirementRange
from flask_app.nlu_pkg.services.classification.relational_handler import RelationalHandler
from flask_app.nlu_pkg.services.utils.spacy_utils import locate_matching_tokens, extract_numbers
from flask_app.nlu_pkg.services.utils.str_utils import parse_number
from flask_app.nlu_pkg.models.enums.parse_status import ParseStatus

PARAMETER_NUMBERS_COUNT = 1
RANGE_NUMBERS_COUNT = 2


class RangeHandler:

    def __init__(self,
                 sentence_tokens: Doc | Span,
                 relational_handler: RelationalHandler,
                 range_patterns: RangePatternsGroup):
        self._tokens = sentence_tokens
        self._range_patterns = range_patterns
        self._relational_bounds = list(relational_handler.extract_relational_bounds(self._tokens))
        self._numbers_in_sentence = extract_numbers(sentence_tokens)
        self._parsing_methods = [
            # Parses using range pattern_groups
            self._process_explicit_range,
            # Parses using relational pattern_groups
            self._process_relational_range,
            # Default parse if parse failed
            self._default_parsing_case
        ]

    def parse_sentence(self) -> ParseResult:
        if self._numbers_in_sentence:
            for parsing_method in self._parsing_methods:
                requirement_range = parsing_method()
                if requirement_range:
                    return ParseResult([requirement_range], self._configure_parse_status(requirement_range))

        return ParseResult([], ParseStatus.UNABLE_TO_PARSE)

    def _configure_parse_status(self, requirement_range: RequirementRange):
        if not requirement_range:
            return ParseStatus.UNABLE_TO_PARSE
        elif requirement_range.end_value - requirement_range.value <= 0:
            return ParseStatus.INVALID_RANGE
        else:
            return ParseStatus.SUCCESSFUL

    def _process_explicit_range(self) -> RequirementRange | None:
        return next(self._range_patterns.match_results(self._tokens), None)

    def _process_relational_range(self) -> RequirementRange | None:
        if len(self._relational_bounds) < RANGE_NUMBERS_COUNT <= len(self._numbers_in_sentence):
            return None
        if len(self._relational_bounds) == PARAMETER_NUMBERS_COUNT:
            return self._extract_range(self._relational_bounds[0])
        elif len(self._relational_bounds) >= RANGE_NUMBERS_COUNT:
            if self._relational_bounds[0].relation_group == self._relational_bounds[1].relation_group:
                comparing_func = max \
                    if self._relational_bounds[0].relation_group == RelationGroup.INCREASED \
                    else min
                return self._extract_range(comparing_func(
                    self._relational_bounds[0],
                    self._relational_bounds[1],
                    key=lambda relational_bound: relational_bound.number_bound))
            else:
                requirement_range = RequirementRange()
                for index in range(RANGE_NUMBERS_COUNT):
                    relational_bound = self._relational_bounds[index]
                    match relational_bound.relation_group:
                        case RelationGroup.INCREASED:
                            requirement_range.value = relational_bound.number_bound
                        case RelationGroup.DECREASED:
                            requirement_range.end_value = relational_bound.number_bound
                return requirement_range

    def _default_parsing_case(self) -> RequirementRange:
        if len(self._numbers_in_sentence) >= RANGE_NUMBERS_COUNT:
            print("DEFAULT PARSING CASE")
            # logging.warning(f"Default parsing case for sentence {self._tokens}, used min, max")
            relevant_numbers = [parse_number(number) for number in self._numbers_in_sentence[:RANGE_NUMBERS_COUNT]]
            return RequirementRange(min(*relevant_numbers), max(*relevant_numbers))
        elif len(self._numbers_in_sentence) == PARAMETER_NUMBERS_COUNT and self._relational_bounds:
            print("DEFAULT PARSING CASE")
            # logging.warning(f"Default parsing case for sentence {self._tokens}, used first relational bound")
            return self._extract_range(self._relational_bounds[0])

    def _extract_range(self, relational_bound: RelationalBound):
        match relational_bound.relation_group:
            case RelationGroup.INCREASED:
                return RequirementRange(relational_bound.number_bound, float("inf"))
            case RelationGroup.DECREASED:
                return RequirementRange(-float("inf"), relational_bound.number_bound)
