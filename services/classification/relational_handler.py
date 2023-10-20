from typing import Tuple, Generator

from nltk.corpus import stopwords
from spacy.matcher import DependencyMatcher
from spacy.tokens import Doc, Span
from definitions import SPACY_MODEL, NEGATION_DEP, CONJUNCTION_DEP
from models.enums.relation_group import RelationGroup
from models.relational_bound import RelationalBound
from services.classification.classifiers.concrete.relational_words_classifier import RelationalWordsClassifier
from services.utils.spacy_utils import find_dependency, extract_tokens
from services.utils.str_utils import parse_number


_RELATIONAL_INDEX_IN_PATTERN = 0
_NUMBER_INDEX_IN_PATTERN = -1

_adjective_pattern = [
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


_verb_pattern = [
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

_adposition_pattern_variation1 = [
    {
        "RIGHT_ID": "first_adposition",
        "RIGHT_ATTRS": {"POS": "ADP"}
    },
    {
        "LEFT_ID": "first_adposition",
        "REL_OP": ".",
        "RIGHT_ID": "second_adposition",
        "RIGHT_ATTRS": {"POS": "ADP"}
    },
    {
        "LEFT_ID": "second_adposition",
        "REL_OP": ".",
        "RIGHT_ID": "number",
        "RIGHT_ATTRS": {"POS": "NUM"}
    }
]

_adposition_pattern_variation2 = [
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


_patterns = [_adjective_pattern, _adposition_pattern_variation1, _adposition_pattern_variation2, _verb_pattern]
class RelationalHandler:
    def __init__(self, relational_classifier: RelationalWordsClassifier):
        self._classifier = relational_classifier
        self._dep_matcher = DependencyMatcher(SPACY_MODEL.vocab)
        self._dep_matcher.add("relational_patterns", _patterns)

    def extract_relational_bounds(self, sentence) -> Generator[RelationalBound, None, None]:
        tokens = SPACY_MODEL(sentence)
        for sentence_chunk in self._split_sentence(tokens):
            chunk_matches = self._dep_matcher(sentence_chunk)
            if chunk_matches:
                match = list(extract_tokens(sentence_chunk, chunk_matches[0]))
                is_reverted = bool(find_dependency(sentence_chunk, NEGATION_DEP))
                try:
                    relation_group: RelationGroup = self._classifier.classify_item(
                        match[_RELATIONAL_INDEX_IN_PATTERN])
                except KeyError:
                    continue
                else:
                    if is_reverted:
                        # revert result if negation exists
                        relation_group = RelationGroup(1 - relation_group.value)
                    number_token = match[_NUMBER_INDEX_IN_PATTERN]
                    yield RelationalBound(relation_group,
                                          parse_number(number_token.text))

    def _split_sentence(self, tokens: Doc) -> Tuple[Span | Doc, ...]:
        conjunction_token = find_dependency(tokens, CONJUNCTION_DEP)
        if conjunction_token:
            return tokens[:conjunction_token.i], tokens[conjunction_token.i + 1:]
        else:
            return tokens,