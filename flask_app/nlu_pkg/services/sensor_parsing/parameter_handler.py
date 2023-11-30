from spacy.tokens import Doc, Span

from ...models.definitions.spacy_def import SPACY_DEP_ATTR, NEGATION_DEP
from ...models.enums.parse_status import ParseStatus
from ...models.named_tuples.range_parse import ParseResult
from ...models.sensor_dto.requirement_param import RequirementParam
from ...models.sensor_dto.requirement_range import RequirementRange
from ..utils.spacy_utils import extract_numbers, locate_matching_token
from ..utils.str_utils import parse_number


def parse_parameter(sentence_tokens: Doc | Span) :
    numbers_in_sentence = extract_numbers(sentence_tokens)
    if numbers_in_sentence:
        # negation exists
        if bool(locate_matching_token(sentence_tokens, SPACY_DEP_ATTR, NEGATION_DEP)):
            bottom_range, upper_range = _parse_negation_parameter(parse_number(numbers_in_sentence[0]))
            return ParseResult([bottom_range, upper_range], ParseStatus.SUCCESSFUL)
        else:
            return ParseResult([RequirementParam(parse_number(numbers_in_sentence[0]))], ParseStatus.SUCCESSFUL)
    else:
        return ParseResult([], ParseStatus.UNABLE_TO_PARSE)

def _parse_negation_parameter(numerical_value):
    return (RequirementRange(float('-inf'), numerical_value),
            RequirementRange(numerical_value + 1, float('inf')))
