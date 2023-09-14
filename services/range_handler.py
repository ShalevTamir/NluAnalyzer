from typing import Callable

import nltk
from nltk import word_tokenize

import definitions
from services.utils.nltk_utils import NUMERICAL_POS_TAG, chunk_sentence, revert_word_pos_tags, find_Nth_in_chunk, \
    COMPARATIVE_ADJECTIVE_POS_TAG
from models.adjective_bound import AdjectiveBound
from models.enums.adjective_group import AdjectiveGroup
from models.requirement_range import RequirementRange
from models.word_pos_tag import WordPosTag
from services.classification.adjective_handler import AdjectiveHandler
from services.sentence_parser import ERROR_MSG


class RangeHandler:
    RANGE_SIZE = 2
    PARAMETER_SIZE = 1
    # Parses syntax like: Engine heat is between 100 and 200
    RANGE_REGEX = r"Chunk: {<" + NUMERICAL_POS_TAG + "><.+>+<" + NUMERICAL_POS_TAG + ">}"

    def __init__(self, adjective_handler_factory: Callable[..., AdjectiveHandler]):
        self.__adjective_handler_factory = adjective_handler_factory

    def __extract_range(self, adjective_bound: AdjectiveBound):
        match adjective_bound.adjective_group:
            case AdjectiveGroup.INCREASED:
                return [adjective_bound.number_bound, float("inf")]
            case AdjectiveGroup.DECREASED:
                return [-float("inf"), adjective_bound.number_bound]

    def __process_adjectives_range(self, comparative_bounds: list[AdjectiveBound]):
        if len(comparative_bounds) == self.PARAMETER_SIZE:
            return self.__extract_range(comparative_bounds[0])

        requirement_range = RequirementRange()
        for index in range(self.RANGE_SIZE):
            comparative_bound = comparative_bounds[index]
            match comparative_bound.adjective_group:
                case AdjectiveGroup.INCREASED:
                    requirement_range.value = comparative_bound.number_bound
                case AdjectiveGroup.DECREASED:
                    requirement_range.end_value = comparative_bound.number_bound
        return requirement_range

    def __process_default_range(self, word_pos_tags: list[WordPosTag]):
        chunk_list = chunk_sentence(word_pos_tags,self.RANGE_REGEX)
        if chunk_list == 0:
            raise ValueError(f"{ERROR_MSG} '{revert_word_pos_tags(word_pos_tags)}'")
        for chunk in chunk_list:
            return RequirementRange(
                    find_Nth_in_chunk(chunk, COMPARATIVE_ADJECTIVE_POS_TAG, 1),
                    find_Nth_in_chunk(chunk, COMPARATIVE_ADJECTIVE_POS_TAG, 2))

    def process_range(self, word_pos_tags: list[WordPosTag]) -> RequirementRange:
        adjective_handler: AdjectiveHandler = self.__adjective_handler_factory(word_pos_tags)
        requirement_range: RequirementRange

        if adjective_handler.has_comparative_adjectives():
            requirement_range = self.__process_adjectives_range(adjective_handler.extract_comparative_bounds())
        else:
            requirement_range = self.__process_default_range(word_pos_tags)

        if requirement_range.value > requirement_range.end_value:
            raise ValueError(f"{ERROR_MSG} '{revert_word_pos_tags(word_pos_tags)}'")
        return requirement_range

