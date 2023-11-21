from typing import Callable, Tuple

from spacy.tokens import Span, Doc, Token

from flask_app.nlu_pkg.models.definitions.spacy_def import SPACY_TEXT_ATTR
from flask_app.nlu_pkg.models.enums.duration_type import DurationType, get_type_text
from flask_app.nlu_pkg.models.enums.noun_type import NounType
from flask_app.nlu_pkg.models.enums.parse_status import ParseStatus
from flask_app.nlu_pkg.models.named_tuples.duration_unit import DurationUnit
from flask_app.nlu_pkg.models.named_tuples.range_parse import ParseResult
from flask_app.nlu_pkg.models.sensor_dto.duration import Duration
from flask_app.nlu_pkg.models.sensor_dto.requirement_param import RequirementParam
from flask_app.nlu_pkg.services.utils.spacy_utils import locate_matching_token, extract_numbers


class DurationHandler:
    def __init__(self, range_handler_factory):
        self._range_handler_factory = range_handler_factory

    def _find_duration_unit(self, sentence: Doc | Span) \
            -> DurationUnit | None:
        # Remove first duration type: undefined
        duration_types = [duration_type for duration_type in DurationType][1:]
        for noun_type in NounType:
            for duration_type in duration_types:
                matching_token = locate_matching_token(
                    sentence,
                    SPACY_TEXT_ATTR,
                    get_type_text(duration_type, noun_type),
                    strong_comparison=True
                )
                if matching_token:
                    return DurationUnit(matching_token, duration_type, noun_type)

    def _parse_plural_duration(self, range_text: Span, duration_type: DurationType) -> Duration:
        if len(range_text) > 1:
            parse_result: ParseResult = self._range_handler_factory(range_text).parse_sentence()
            if parse_result.parse_status == ParseStatus.SUCCESSFUL:
                return Duration(
                    duration_type,
                    parse_result.requirement
                )
        else:
            return Duration(
                duration_type,
                extract_numbers(range_text)[0]
            )

    def _parse_singular_duration(self, duration_type: DurationType) -> Duration:
        return Duration(
            duration_type,
            RequirementParam(1)
        )

    def _duration_unit_to_duration(self, sentence: Doc | Span, duration_unit: DurationUnit):
        duration_token, duration_type, noun_type = duration_unit
        match noun_type:
            case NounType.PLURAL:
                return self._parse_plural_duration(
                    sentence[duration_token.head.i:duration_token.i-1],
                    duration_type
                )
            case NounType.SINGULAR:
                return self._parse_singular_duration(
                    duration_type
                )

    def _cut_duration_text(self, sentence: Doc | Span, duration_token: Token):
        return sentence[:duration_token.head.i - 1]

    def extract_duration(self, sentence: Doc | Span) -> Tuple[Doc | Span, Duration]:
        """ Returns the refined sentence without the duration text and the duration itself """
        duration_unit = self._find_duration_unit(sentence)
        if duration_unit:
            duration = self._duration_unit_to_duration(sentence, duration_unit)
            sentence = self._cut_duration_text(sentence, duration_unit.duration_token)
        else:
            duration = Duration(
                DurationType.UNDEFINED,
                None
            )
        return sentence, duration
