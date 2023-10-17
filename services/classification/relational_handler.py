from itertools import islice, takewhile
from typing import Iterable, Tuple, Generator

import nltk
import spacy
from nltk import WordNetLemmatizer, Tree
from spacy.matcher import DependencyMatcher
from spacy.tokens import Doc, Token, Span

from definitions import COMPARATIVE_ADJECTIVE_POS_TAG, NUMERICAL_POS_TAG, CONJUNCTION_POS_TAG, SPACY_MODEL
from models.enums.relation_group import RelationGroup
from services.classification.word_embedding.concrete.word2vec_embedder import Word2VecEmbedder
from services.utils.nltk_utils import chunk_sentence, find_Nth_in_chunk
from models.relational_bound import RelationalBound
from models.word_pos_tag import WordPosTag
from services.classification.classifiers.concrete.relational_words_classifier import RelationalWordsClassifier
from services.utils.str_utils import parse_number
from services.utils.spacy_utils import find_dependency, extract_tokens

CONJUNCTION_DEP = 'cc'
RELATIONAL_INDEX_IN_PATTERN = 0
NUMBER_INDEX_IN_PATTERN = -1

adjective_pattern = [
    {
        "RIGHT_ID": "adjective",
        "RIGHT_ATTRS": {"POS": "ADJ"}
    },
    {
        "LEFT_ID": "adjective",
        "REL_OP": ".",
        "RIGHT_ID": "adposition",
        "RIGHT_ATTRS": {"POS": "ADP"}
    },
    {
        "LEFT_ID": "adposition",
        "REL_OP": ".",
        "RIGHT_ID": "number",
        "RIGHT_ATTRS": {"POS": "NUM"}
    }
]

adposition_pattern = [
    {
        "RIGHT_ID": "adposition",
        "RIGHT_ATTRS": {"POS": "ADP"}
    },
    {
        "LEFT_ID": "adposition",
        "REL_OP": ".",
        "RIGHT_ID": "number",
        "RIGHT_ATTRS": {"POS": "NUM"}
    }
]

verb_pattern = [
    {
        "RIGHT_ID": "verb",
        "RIGHT_ATTRS": {"POS": "VERB"}
    },
    {
        "LEFT_ID": "verb",
        "REL_OP": ".",
        "RIGHT_ID": "number",
        "RIGHT_ATTRS": {"POS": "NUM"}
    }
]

patterns = [adjective_pattern, adposition_pattern, verb_pattern]

class RelationalHandler:
    def __init__(self, relational_classifier: RelationalWordsClassifier):
        self.__classifier = relational_classifier
        self.__dep_matcher = DependencyMatcher(SPACY_MODEL.vocab)
        self.__dep_matcher.add("relational_patterns", patterns)

    def extract_relational_bounds(self, sentence) -> Generator[RelationalBound, None, None]:
        tokens = SPACY_MODEL(sentence)
        matches = [list(extract_tokens(sentence_chunk, chunk_matches[0]))
                   for sentence_chunk in self.__split_sentence(tokens)
                   if (chunk_matches := self.__dep_matcher(sentence_chunk))]

        for match in matches:
            relational_word_token = match[RELATIONAL_INDEX_IN_PATTERN]
            number_token = match[NUMBER_INDEX_IN_PATTERN]
            relational_bound = RelationalBound(self.__classifier.classify_item(relational_word_token),
                                               parse_number(number_token.text))
            yield relational_bound

    def __split_sentence(self, tokens: Doc) -> Tuple[Span | Doc, ...]:
        conjunction_token = find_dependency(tokens, CONJUNCTION_DEP)
        if conjunction_token:
            return tokens[:conjunction_token.i], tokens[conjunction_token.i + 1:]
        else:
            return tokens,
