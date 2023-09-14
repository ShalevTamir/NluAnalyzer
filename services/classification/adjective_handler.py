import nltk
from nltk import WordNetLemmatizer, Tree

from services.utils.nltk_utils import COMPARATIVE_ADJECTIVE_POS_TAG, NUMERICAL_POS_TAG, CONJUNCTION_POS_TAG, \
    chunk_sentence,find_Nth_in_chunk
from models.adjective_bound import AdjectiveBound
from models.word_pos_tag import WordPosTag
from services.classification.classifiers.concrete.adjective_classifier import AdjectiveClassifier


class AdjectiveHandler:
    COMPERATIVE_BOUND_REGEX = r"Chunk: {<" + COMPARATIVE_ADJECTIVE_POS_TAG + ">\
                                <" + CONJUNCTION_POS_TAG + ">\
                                <" + NUMERICAL_POS_TAG + ">}"

    def __init__(self, adjective_classifier: AdjectiveClassifier, word_pos_tags: list[WordPosTag]):
        self.__lemmatizer = WordNetLemmatizer()
        self.__classifier = adjective_classifier
        self.__word_pos_tags = word_pos_tags

    def has_comparative_adjectives(self) -> bool:
        # ASK: bad because initializing new list just to count?
        comparative_adjectives = [word_pos_tag
                                  for word_pos_tag in self.__word_pos_tags
                                  if word_pos_tag.pos_tag == COMPARATIVE_ADJECTIVE_POS_TAG]
        return len(comparative_adjectives) > 0

    def extract_comparative_bounds(self) -> list[AdjectiveBound]:
        chunked_sentence = chunk_sentence(self.__word_pos_tags, self.COMPERATIVE_BOUND_REGEX)
        adjective_bounds: list[AdjectiveBound] = []
        for chunk in chunked_sentence:
            adjective = find_Nth_in_chunk(chunk, NUMERICAL_POS_TAG, 1)
            number_bound = find_Nth_in_chunk(chunk, COMPARATIVE_ADJECTIVE_POS_TAG, 1)
            adjective_bounds.append(AdjectiveBound(
                self.__classifier.classify_item(adjective),
                number_bound
            ))

        return adjective_bounds
