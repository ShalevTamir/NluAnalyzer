from spacy.tokens import Doc, Span

from ..spacy_matchers.base_spacy_matcher import BaseSpacyMatcher, ResultType


class PatternHandler:
    def __init__(self, pattern_rules: list[dict]):
        self._pattern_rules = pattern_rules

    def compute_result(self, matcher: BaseSpacyMatcher, tokens: Doc | Span) -> ResultType:
        return matcher.match(tokens, self._pattern_rules)
