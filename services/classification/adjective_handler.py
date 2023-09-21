import nltk
from nltk import WordNetLemmatizer, Tree
from definitions import COMPARATIVE_ADJECTIVE_POS_TAG, NUMERICAL_POS_TAG, CONJUNCTION_POS_TAG
from services.utils.nltk_utils import chunk_sentence, find_Nth_in_chunk
from models.adjective_bound import AdjectiveBound
from models.word_pos_tag import WordPosTag
from services.classification.classifiers.concrete.adjective_classifier import AdjectiveClassifier
from services.utils.str_utils import parse_number


class AdjectiveHandler:
    def __init__(self, adjective_classifier: AdjectiveClassifier):
        self.__classifier = adjective_classifier

    def extract_comparative_bounds(self, chunk_list: list[list[WordPosTag]]) -> list[AdjectiveBound]:
        adjective_bounds: list[AdjectiveBound] = []
        for chunk in chunk_list:
            adjective = find_Nth_in_chunk(chunk, COMPARATIVE_ADJECTIVE_POS_TAG, 1)
            number_bound = find_Nth_in_chunk(chunk, NUMERICAL_POS_TAG, 1)
            adjective_bounds.append(AdjectiveBound(
                self.__classifier.classify_item(self.__lemmatizer.lemmatize(adjective)),
                parse_number(number_bound)
            ))

        return adjective_bounds
