from typing import Tuple, Generator
from spacy.tokens import Doc, Span

from models.definitions.spacy_def import SPACY_MODEL, SPACY_DEP_ATTR, NEGATION_DEP, NUMERICAL_POS_TAG, SPACY_POS_ATTR
from models.enums.relation_group import RelationGroup, revert_relation_group
from models.named_tuples.relational_bound import RelationalBound
from models.patterns_matcher.relational_matcher import RelationalMatcher
from services.utils.spacy_utils import locate_matching_token


class RelationalHandler:
    def __init__(self, relational_matcher: RelationalMatcher):
        self._relational_matcher = relational_matcher

    def extract_relational_bounds(self, tokens: Span | Doc) -> Generator[RelationalBound, None, None]:
        for sentence_chunk in self._split_sentence(tokens):
            for pattern_result in self._relational_matcher.match_results(sentence_chunk):
                yield self._revert_negated_bound(sentence_chunk, pattern_result)
                break

    def _split_sentence(self, sentence_chunk: Span) -> Tuple[Span, ...]:
        first_number = locate_matching_token(sentence_chunk, SPACY_POS_ATTR, NUMERICAL_POS_TAG)
        first_number_index = first_number.i - sentence_chunk.start if isinstance(sentence_chunk, Span) else first_number.i
        if not first_number or first_number_index == len(sentence_chunk) - 1:
            return sentence_chunk,
        else:
            return sentence_chunk[:first_number_index + 1], sentence_chunk[first_number_index + 1:]

    def _revert_negated_bound(self, sentence_chunk: Doc | Span, relational_bound: RelationalBound):
        # negation detected
        if bool(locate_matching_token(sentence_chunk, SPACY_DEP_ATTR, NEGATION_DEP)):
            return RelationalBound(revert_relation_group(relational_bound.relation_group), relational_bound.number_bound)
        else:
            return relational_bound
