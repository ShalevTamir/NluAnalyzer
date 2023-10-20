from typing import Tuple, Generator

from nltk.corpus import stopwords
from spacy.matcher import DependencyMatcher
from spacy.tokens import Doc, Span
from definitions import SPACY_MODEL
from models.enums.relation_group import RelationGroup
from models.relational_bound import RelationalBound
from services.classification.classifiers.concrete.relational_words_classifier import RelationalWordsClassifier
from services.utils.spacy_utils import find_dependency, extract_tokens
from services.utils.str_utils import parse_number

CONJUNCTION_DEP = 'cc'
NEGATION_DEP = 'neg'
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
        for sentence_chunk in self.__split_sentence(tokens):
            chunk_matches = self.__dep_matcher(sentence_chunk)
            if chunk_matches:
                match = list(extract_tokens(sentence_chunk, chunk_matches[0]))
                if match[RELATIONAL_INDEX_IN_PATTERN].text in stopwords.words('english'):
                    is_reverted = bool(find_dependency(sentence_chunk, NEGATION_DEP))
                    try:
                        relation_group: RelationGroup = self.__classifier.classify_item(
                            match[RELATIONAL_INDEX_IN_PATTERN])
                    except KeyError:
                        continue
                    if is_reverted:
                        # revert result if negation exists
                        relation_group = RelationGroup(1 - relation_group.value)
                    number_token = match[NUMBER_INDEX_IN_PATTERN]
                    yield RelationalBound(relation_group,
                                          parse_number(number_token.text))

    def __split_sentence(self, tokens: Doc) -> Tuple[Span | Doc, ...]:
        conjunction_token = find_dependency(tokens, CONJUNCTION_DEP)
        if conjunction_token:
            return tokens[:conjunction_token.i], tokens[conjunction_token.i + 1:]
        else:
            return tokens,
