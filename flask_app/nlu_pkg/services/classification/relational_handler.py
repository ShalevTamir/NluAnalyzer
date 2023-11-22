from typing import Tuple, Generator
from spacy.tokens import Doc, Span
from flask_app.nlu_pkg.models.definitions.spacy_def import NUMERICAL_POS_TAG, SPACY_POS_ATTR, SPACY_DEP_ATTR, \
    NEGATION_DEP, RELATIVE_INDEX
from flask_app.nlu_pkg.models.enums.relation_group import revert_relation_group
from flask_app.nlu_pkg.models.named_tuples.relational_bound import RelationalBound
from flask_app.nlu_pkg.models.pattern_groups.relational_patterns_group import RelationalPatternsGroup
from flask_app.nlu_pkg.services.utils.spacy_utils import locate_matching_token


class RelationalHandler:
    def __init__(self, relational_patterns: RelationalPatternsGroup):
        self._relational_patterns = relational_patterns

    def extract_relational_bounds(self, tokens: Span | Doc) -> Generator[RelationalBound, None, None]:
        for sentence_chunk in self._split_sentence(tokens):
            first_pattern_match = next(self._relational_patterns.match_results(sentence_chunk), None)
            if first_pattern_match:
                yield self._revert_negated_bound(sentence_chunk, first_pattern_match)

    def _split_sentence(self, sentence_chunk: Span) -> Tuple[Span, ...]:
        first_number = locate_matching_token(sentence_chunk, SPACY_POS_ATTR, NUMERICAL_POS_TAG)
        if not first_number or first_number.i - sentence_chunk.start == len(sentence_chunk) - 1:
            return sentence_chunk,
        else:
            return (sentence_chunk[:sentence_chunk._.get(RELATIVE_INDEX)(first_number) + 1],
                    sentence_chunk[sentence_chunk._.get(RELATIVE_INDEX)(first_number) + 1:])

    def _revert_negated_bound(self, sentence_chunk: Doc | Span, relational_bound: RelationalBound):
        # negation detected
        if bool(locate_matching_token(sentence_chunk, SPACY_DEP_ATTR, NEGATION_DEP)):
            return RelationalBound(revert_relation_group(relational_bound.relation_group), relational_bound.number_bound)
        else:
            return relational_bound
