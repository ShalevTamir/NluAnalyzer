import json
from functools import partial
from typing import Tuple

from flask_app.services.json.custom_encoder import CustomEncoder
from models.enums.parse_status import ParseStatus
from models.enums.sentence_group import SentenceGroup
from models.named_tuples.range_parse import ParseResult
from models.sensor_dto.requirement_param import RequirementParam
from models.sensor_dto.sensor import Sensor
from services.classification.classifiers.concrete.sentence_classifier import SentenceClassifier
from services.classification.preprocessing.preprocessor import remove_punctuation_marks
from services.sensor_parsing.range_handler import RangeHandler
from services.sensor_parsing.subject_detector import SubjectDetector
from services.sensor_parsing.text_partitioner import TextPartitioner
from services.utils.str_utils import extract_numbers


class TextParser:
    def __init__(self,
                 subject_detector: SubjectDetector,
                 sentence_classifier: SentenceClassifier,
                 range_handler_factory,
                 text_partitioner: TextPartitioner):
        self._param_detector = subject_detector
        self._sentence_classifier = sentence_classifier
        self._range_handler_factory = range_handler_factory
        self._text_partitioner = text_partitioner

    def _parse_range(self, sentence) -> ParseResult:
        return self._range_handler_factory(sentence).parse_sentence()

    def _parse_parameter(self, sentence) -> ParseResult:
        numbers_in_sentence = extract_numbers(sentence)
        if numbers_in_sentence:
            return ParseResult(RequirementParam(numbers_in_sentence[0]), ParseStatus.SUCCESSFUL)
        else:
            return ParseResult(None, ParseStatus.UNABLE_TO_PARSE)

    def _parse_sentence_by_type(self, sentence: str, sentence_type: SentenceGroup) \
            -> ParseResult:
        return self._parse_range(sentence) \
            if sentence_type == SentenceGroup.RANGE \
            else self._parse_parameter(sentence)

    def parse(self, text: str):
        sentence = remove_punctuation_marks(text)
        parameter_name = self._param_detector.detect(sentence)
        sentence_type: SentenceGroup = self._sentence_classifier.classify_item(sentence)
        # containing the methods used to parse and their arguments
        parsing_options = [partial(self._parse_sentence_by_type, sentence, sentence_type),
                           partial(self._parse_sentence_by_type, sentence, SentenceGroup(1 - sentence_type.value))]

        parse_result: ParseResult = ParseResult(None, ParseStatus.UNABLE_TO_PARSE)
        for parsing_option in parsing_options:
            parse_result: ParseResult = parsing_option()
            if parse_result.parse_status == ParseStatus.SUCCESSFUL:
                return Sensor(parameter_name, parse_result.requirement)
            elif parse_result.parse_status == ParseStatus.INVALID_RANGE:
                raise ValueError(f"Invalid range for sentence {sentence}, "
                                 f"parsed {json.dumps(Sensor(parameter_name, parse_result.requirement), cls=CustomEncoder)}")

        if parse_result.parse_status == ParseStatus.UNABLE_TO_PARSE:
            raise ValueError(f"Unable to parse sentence {sentence}")
