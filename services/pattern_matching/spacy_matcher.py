from spacy.matcher import Matcher
from spacy.tokens import Doc, Span

from models.definitions.spacy_def import SPACY_MODEL
from services.pattern_matching.pattern import Pattern


class SpacyMatcher:
    def __init__(self, patterns: list[Pattern]):
        self._matcher = Matcher(SPACY_MODEL.vocab)
        self._patterns = patterns

    def pattern_results(self, tokens: Doc | Span):
        for pattern in self._patterns:
            yield pattern.compute_result(self._matcher, tokens)

