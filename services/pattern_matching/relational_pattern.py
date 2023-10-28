from spacy.matcher import Matcher
from spacy.tokens import Doc, Span

from models.enums.relation_group import RelationGroup, revert_relation_group
from models.named_tuples.relational_bound import RelationalBound
from services.classification.classifiers.concrete.relational_words_classifier import RelationalWordsClassifier
from services.pattern_matching.pattern import Pattern
from services.utils.str_utils import parse_number


class RelationalPattern(Pattern):
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

    def compute_result(self, matcher: Matcher, tokens: Doc | Span) -> RelationalBound:
        match = super().compute_result(matcher, tokens)
        if match:
            relational_token = match[self._relational_index]
            try:
                relation_group: RelationGroup = self._relational_classifier.classify_item(relational_token)
            except KeyError:
                pass
            else:
                if self._reverse_classification:
                    relation_group = revert_relation_group(relation_group)
                number_token = match[self._number_index]
                return RelationalBound(relation_group, parse_number(number_token.text))

