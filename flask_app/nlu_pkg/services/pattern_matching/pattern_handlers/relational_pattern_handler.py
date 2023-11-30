from spacy.tokens import Doc, Span

from ....models.enums.relation_group import RelationGroup, revert_relation_group
from ....models.named_tuples.relational_bound import RelationalBound
from ...classification.classifiers.concrete.relational_words_classifier import RelationalWordsClassifier
from .pattern_handler import PatternHandler
from ..spacy_matchers.spacy_matcher import SpacyMatcher
from ...utils.str_utils import parse_number


class RelationalPatternHandler(PatternHandler):
    def __init__(self,
                 pattern_rules: list[dict],
                 relational_classifier: RelationalWordsClassifier,
                 relational_index: int = 0,
                 number_index: int = -1,
                 reverse_classification=False):
        super().__init__(pattern_rules)
        self._relational_classifier = relational_classifier
        self._relational_index = relational_index
        self._number_index = number_index
        self._reverse_classification = reverse_classification

    def compute_result(self, matcher: SpacyMatcher, tokens: Doc | Span) -> RelationalBound:
        first_match = next(iter(super().compute_result(matcher, tokens)), None)
        if first_match:
            print(f"RELATIONAL MATCH {first_match}")
            relational_token = first_match[self._relational_index]
            try:
                relation_group: RelationGroup = self._relational_classifier.classify_item(relational_token)
            except KeyError:
                pass
            else:
                # print("RELATIONAL MATCH ", self._pattern_rules, first_match, relation_group)
                if self._reverse_classification:
                    relation_group = revert_relation_group(relation_group)
                number_token = first_match[self._number_index]
                return RelationalBound(relation_group, parse_number(number_token.text))

