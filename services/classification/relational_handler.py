from typing import Tuple, Generator

from nltk.corpus import stopwords
from spacy.matcher import DependencyMatcher
from spacy.tokens import Doc, Span
from definitions import SPACY_MODEL, NEGATION_DEP, CONJUNCTION_DEP, NUMERICAL_POS_TAG_SPACY
from models.enums.relation_group import RelationGroup
from models.relational_bound import RelationalBound
from services.classification.classifiers.concrete.relational_words_classifier import RelationalWordsClassifier
from services.utils.spacy_utils import extract_tokens, locate_matching_token
from services.utils.str_utils import parse_number
from models.named_tuples.pattern import patterns

class RelationalHandler:
    def __init__(self, relational_classifier: RelationalWordsClassifier):
        self._classifier = relational_classifier
        self._dep_matcher = DependencyMatcher(SPACY_MODEL.vocab)
        # self._dep_matcher.add("relational_patterns", _patterns)

    def extract_relational_bounds(self, sentence) -> Generator[RelationalBound, None, None]:
        tokens = SPACY_MODEL(sentence)
        for sentence_chunk in self._split_sentence(tokens):
            for current_pattern in patterns:
                self._dep_matcher.add("current_pattern", [current_pattern.pattern_rules])
                chunk_matches = self._dep_matcher(sentence_chunk)
                self._dep_matcher.remove("current_pattern")
                if chunk_matches:
                    match = list(extract_tokens(sentence_chunk, chunk_matches[0]))
                    is_reverted = current_pattern.is_reversed or \
                                  bool(locate_matching_token(sentence_chunk, 'dep_', NEGATION_DEP))
                    try:
                        relation_group: RelationGroup = self._classifier.classify_item(
                            match[current_pattern.relational_index])
                    except KeyError:
                        continue
                    else:
                        if is_reverted:
                            # revert result if negation exists
                            relation_group = RelationGroup(1 - relation_group.value)
                        number_token = match[current_pattern.number_index]
                        yield RelationalBound(relation_group,
                                              parse_number(number_token.text))
                        break

    def _split_sentence(self, tokens: Doc) -> Tuple[Span | Doc, ...]:
        first_number = locate_matching_token(tokens, 'pos_', NUMERICAL_POS_TAG_SPACY)
        if first_number.i == len(tokens) - 1:
            return tokens,
        else:
            return tokens[:first_number.i + 1], tokens[first_number.i + 1:]
