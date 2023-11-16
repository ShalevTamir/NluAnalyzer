from functools import partial

from spacy import displacy
from spacy.tokens import Span, Doc, Token

from flask_app.nlu_pkg.models.definitions.spacy_def import SPACY_DEP_ATTR, SUBJECT_DEP, ROOT_DEP, SPACY_TEXT_ATTR, NER_MODEL, STOP_WORDS
from flask_app.nlu_pkg.models.pattern_groups.subject_patterns_group import SubjectPatternsGroup
from flask_app.nlu_pkg.services.utils.spacy_utils import locate_matching_token, locate_matching_tokens

# _SUBJ_DEPENDENCIES = [SUBJECT_DEP, ROOT_DEP]
_SUBJ_SPACE_CHAR = '_'
from flask_app.nlu_pkg.models.definitions.spacy_def import SPACY_MODEL
import spacy

class SubjectDetector:
    def __init__(self, subject_patterns: SubjectPatternsGroup):
        self._subject_patterns = subject_patterns

    def detect(self, tokens: Doc | Span, multiple=False, as_text=False):
        if multiple:
            return self._detect_subjects(tokens, as_text)
        else:
            return next(self._detect_subjects(tokens, as_text), None)

    def _detect_subjects(self, tokens: Doc | Span, as_text):
        yielded_subjects = set()
        test = partial(locate_matching_tokens, tokens, SPACY_DEP_ATTR, SUBJECT_DEP)
        subject_locators = [
            # partial(locate_matching_tokens, tokens, SPACY_TEXT_ATTR, _SUBJ_SPACE_CHAR),
            partial(self._detect_custom_ner, tokens),
            test,
            # partial(self._match_subject_patterns, tokens)
        ]
        default_subject_locator = partial(locate_matching_token, tokens, SPACY_DEP_ATTR, ROOT_DEP)
        for subject_locator in subject_locators:
            subjects = subject_locator()
            if subject_locator == test:
                subjects = list(subjects)
                print(subjects, "SPACY")
            for subject in subjects:
                if subject.i not in yielded_subjects and subject.text not in STOP_WORDS and not subject.like_num:
                    yield subject.text if as_text else subject
                    yielded_subjects.add(subject.i)

        if not yielded_subjects:
            yield default_subject_locator()

    def _detect_custom_ner(self, tokens: Doc | Span):
        tokens = NER_MODEL(tokens.text)
        result = [ent_span[0] for ent_span in tokens.ents]
        print(result, "NER")
        return [ent_span[0] for ent_span in tokens.ents]

    def _match_subject_patterns(self, tokens: Doc | Span):
        extracted_subjects = []
        for match_result in self._subject_patterns.match_results(tokens):
            extracted_subjects += match_result
        print(extracted_subjects,"PATTERN SUBJECT")
        return extracted_subjects
