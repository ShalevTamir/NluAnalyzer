from abc import ABC
from typing import Iterable, Generator

from spacy.tokens import Doc, Span

from flask_app.nlu_pkg.services.pattern_matching.pattern_handlers.pattern_handler import PatternHandler
from flask_app.nlu_pkg.services.pattern_matching.spacy_matchers.base_spacy_matcher import BaseSpacyMatcher, ResultType


class PatternsGroup(ABC):
    def __init__(self, matcher: BaseSpacyMatcher, patterns: list[PatternHandler]):
        self._patterns = patterns
        self._matcher = matcher

    def match_results(self, tokens: Doc | Span) -> Generator[ResultType, None, None]:
        for pattern in self._patterns:
            pattern_result = pattern.compute_result(self._matcher, tokens)
            if pattern_result:
                yield pattern_result

