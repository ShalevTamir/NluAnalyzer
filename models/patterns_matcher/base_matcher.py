from abc import ABC

from spacy.matcher import Matcher
from spacy.tokens import Doc, Span

from models.definitions.spacy_def import SPACY_MODEL
from services.pattern_matching.pattern import Pattern


class PatternsMatcher(ABC):
    def __init__(self, patterns: list[Pattern]):
        self._patterns = patterns
        self._matcher = Matcher(SPACY_MODEL.vocab)

    def match_results(self, tokens: Doc | Span):
        for pattern in self._patterns:
            pattern_result = pattern.compute_result(self._matcher, tokens)
            if pattern_result:
                yield pattern_result

