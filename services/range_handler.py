import json

from numpy import minimum, maximum
from definitions import NUMERICAL_POS_TAG, ADJECTIVE_OR_NUMERICAL_POS_TAG, \
    RANGE_NUMBERS_COUNT, PARAMETER_NUMBERS_COUNT
from flask_app.services.json.custom_encoder import CustomEncoder
from models.enums.relation_group import RelationGroup
from models.relational_bound import RelationalBound
from models.requirement_range import RequirementRange
from services.classification.relational_handler import RelationalHandler
from services.utils.nltk_utils import chunk_sentence, find_Nth_in_chunk, \
    validate_number_detection, extract_word_pos_tags
from services.utils.nltk_utils import extract_numbers as extract_numbers_nltk
from services.utils.str_utils import parse_number


_IMPLICIT_RANGE_REGEX = r"Chunk: {<" + NUMERICAL_POS_TAG + "><.+><" + NUMERICAL_POS_TAG + ">}"
_EXPLICIT_RANGE_REGEX = r"Chunk: {<" + ADJECTIVE_OR_NUMERICAL_POS_TAG + ">}"


class RangeHandler:

    def __init__(self, sentence: str, relational_handler: RelationalHandler):
        self._relational_handler = relational_handler
        self._sentence = sentence
        self._word_pos_tags = extract_word_pos_tags(sentence)
        self._relational_bounds = None

    def parse_sentence(self) -> RequirementRange:
        validate_number_detection(self._word_pos_tags)
        parsing_methods = [
            # Parses syntax: Engine heat is between 100 and 200
            self._process_implicit_range,
            # Parses syntax: Engine heat in range 100-200
            self._process_explicit_range,
            # Parses syntax: Engine heat is greater than 50
            self._process_relational_range,
            # Default parse if not parse succeeded
            self._default_parsing_case
        ]

        for parsing_method in parsing_methods:
            requirement_range = parsing_method()
            if not requirement_range:
                continue
            # validate range
            if requirement_range.end_value - requirement_range.value > 0:
                return requirement_range
            else:
                raise ValueError(f'Invalid range {json.dumps(requirement_range, cls=CustomEncoder)}')

    def _process_implicit_range(self) -> RequirementRange:
        chunk_list = chunk_sentence(self._word_pos_tags, _IMPLICIT_RANGE_REGEX)
        for chunk in chunk_list:
            return RequirementRange(
                parse_number(find_Nth_in_chunk(chunk, NUMERICAL_POS_TAG, 1)),
                parse_number(find_Nth_in_chunk(chunk, NUMERICAL_POS_TAG, 2)))

    def _process_explicit_range(self) -> RequirementRange:
        numbers_in_sentence = [number.word for number in extract_numbers_nltk(self._word_pos_tags)]
        for number in numbers_in_sentence:
            possible_range = number.split('-')
            if len(possible_range) == 2:
                try:
                    lower_range_value = parse_number(possible_range[0])
                    higher_range_value = parse_number(possible_range[1])
                except ValueError:
                    pass
                else:
                    return RequirementRange(
                        lower_range_value,
                        higher_range_value
                    )

    def _process_relational_range(self) -> RequirementRange:
        if len(self._get_relational_bounds()) == PARAMETER_NUMBERS_COUNT:
            return self._extract_range(self._get_relational_bounds()[0])
        elif len(self._get_relational_bounds()) >= RANGE_NUMBERS_COUNT:
            requirement_range = RequirementRange()
            for index in range(RANGE_NUMBERS_COUNT):
                relational_bound = self._get_relational_bounds()[index]
                match relational_bound.relation_group:
                    case RelationGroup.INCREASED:
                        requirement_range.value = relational_bound.number_bound
                    case RelationGroup.DECREASED:
                        requirement_range.end_value = relational_bound.number_bound
            return requirement_range

    def _default_parsing_case(self) -> RequirementRange:
        numbers_in_sentence = [parse_number(number.word) for number in extract_numbers_nltk(self._word_pos_tags)]
        if len(numbers_in_sentence) >= RANGE_NUMBERS_COUNT:
            relevant_numbers = [numbers_in_sentence[0], numbers_in_sentence[1]]
            return RequirementRange(minimum(*relevant_numbers), maximum(*relevant_numbers))
        elif len(numbers_in_sentence) == PARAMETER_NUMBERS_COUNT and self._get_relational_bounds():
            return self._extract_range(self._get_relational_bounds()[0])

    def _extract_range(self, relational_bound: RelationalBound):
        match relational_bound.relation_group:
            case RelationGroup.INCREASED:
                return RequirementRange(relational_bound.number_bound, float("inf"))
            case RelationGroup.DECREASED:
                return RequirementRange(-float("inf"), relational_bound.number_bound)


    def _get_relational_bounds(self):
        if self._relational_bounds is None:
            self._relational_bounds = list(self._relational_handler.extract_relational_bounds(self._sentence))
        return self._relational_bounds
