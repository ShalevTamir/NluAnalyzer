from typing import Generator, Iterator

from spacy.tokens import Doc, Span, Token

from services.pattern_matching.pattern_handlers.pattern_handler import PatternHandler
from services.pattern_matching.spacy_matchers.spacy_dependency_matcher import SpacyDependencyMatcher


class SubjectPatternHandler(PatternHandler):
    def __init__(self, pattern_rules: list[dict], subject_index=-1):
        super().__init__(pattern_rules)
        self._subject_index = subject_index

    def compute_result(self, matcher: SpacyDependencyMatcher, tokens: Doc | Span) -> list[Token]:
        return [
            match[self._subject_index]
            for match in super().compute_result(matcher, tokens)
        ]
        # yield from (match[-1] for match in super().compute_result(matcher, tokens))


