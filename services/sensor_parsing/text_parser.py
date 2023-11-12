import json
import logging
from functools import partial
from typing import Tuple

from spacy.tokens import Span, Doc

from flask_app.services.json.custom_encoder import CustomEncoder
from models.definitions.spacy_def import SPACY_MODEL, SPAN_SUBJECT_ATTR
from models.enums.parse_status import ParseStatus
from models.enums.sentence_group import SentenceGroup
from models.named_tuples.range_parse import ParseResult
from models.sensor_dto.requirement_param import RequirementParam
from models.sensor_dto.sensor import Sensor
from services.classification.classifiers.concrete.sentence_classifier import SentenceClassifier
from services.classification.preprocessing.preprocessor import remove_punctuation_marks
from services.sensor_parsing.subject_detector import SubjectDetector
from services.sensor_parsing.text_partitioner import TextPartitioner
from services.utils.spacy_utils import extract_numbers
from services.utils.str_utils import parse_number


class TextParser:
    def __init__(self,
                 sentence_classifier: SentenceClassifier,
                 text_partitioner: TextPartitioner,
                 subject_detector: SubjectDetector,
                 range_handler_factory):
        self._sentence_classifier = sentence_classifier
        self._text_partitioner = text_partitioner
        self._subject_detector = subject_detector
        self._range_handler_factory = range_handler_factory

    def _parse_range(self, sentence_tokens: Doc | Span) -> ParseResult:
        return self._range_handler_factory(sentence_tokens).parse_sentence()

    def _parse_parameter(self, sentence_tokens: Doc | Span) -> ParseResult:
        numbers_in_sentence = extract_numbers(sentence_tokens)
        if numbers_in_sentence:
            return ParseResult(RequirementParam(parse_number(numbers_in_sentence[0])), ParseStatus.SUCCESSFUL)
        else:
            return ParseResult(None, ParseStatus.UNABLE_TO_PARSE)

    def _parse_sentence_by_type(self, sentence_tokens: Doc | Span, sentence_type: SentenceGroup) \
            -> ParseResult:
        return self._parse_range(sentence_tokens) \
            if sentence_type == SentenceGroup.RANGE \
            else self._parse_parameter(sentence_tokens)

    def parse(self, text: str):
        text = remove_punctuation_marks(text)
        tokens = SPACY_MODEL(text)
        for sentence_tokens in self._text_partitioner.extract_sentences(tokens):
            # parameter_name = self._subject_detector.detect(sentence_tokens, as_text=True, multiple=False)
            parameter_name = sentence_tokens._.get(SPAN_SUBJECT_ATTR).text
            sentence_type: SentenceGroup = self._sentence_classifier.classify_item(sentence_tokens.text)
            # containing the methods used to parse and their arguments
            parsing_options = [partial(self._parse_sentence_by_type, sentence_tokens, sentence_type),
                               partial(self._parse_sentence_by_type, sentence_tokens, SentenceGroup(1 - sentence_type.value))]

            parse_result: ParseResult = ParseResult(None, ParseStatus.UNABLE_TO_PARSE)
            for parsing_option in parsing_options:
                parse_result: ParseResult = parsing_option()
                if parse_result.parse_status == ParseStatus.SUCCESSFUL:
                    yield Sensor(parameter_name, parse_result.requirement)
                    break
                elif parse_result.parse_status == ParseStatus.INVALID_RANGE:
                    raise ValueError(f"Invalid range for sentence {sentence_tokens.text}, "
                                     f"parsed {json.dumps(Sensor(parameter_name, parse_result.requirement), cls=CustomEncoder)}")

            # if parse_result.parse_status == ParseStatus.UNABLE_TO_PARSE:
            #     logging.warning(f"Unable to parse sentence {sentence_tokens.text}")
                # raise ValueError(f"Unable to parse sentence {sentence_tokens}")
