from spacy.matcher import Matcher
from spacy.tokens import Doc, Span

from services.utils.spacy_utils import extract_tokens


class Pattern:
    def __init__(self, pattern_rules: list[dict]):
        self._pattern_rules = pattern_rules

    def compute_result(self, matcher: Matcher, tokens: Doc | Span):
        matcher.add("", [self._pattern_rules])
        results = matcher(tokens, as_spans=True)
        matcher.remove("")
        return results[0] if results else []

    pattern_rules = property(fget=lambda self: self._pattern_rules)
