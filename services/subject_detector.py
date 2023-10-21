from functools import partial

from spacy.tokens.token import Token
from definitions import SPACY_MODEL
from services.utils.spacy_utils import locate_matching_token


class SubjectDetector:
    _SUBJ_DEPENDENCIES = ["subj", "ROOT"]
    _SUBJ_SPACE_CHAR = '_'

    def detect(self, sentence: str):
        tokens = SPACY_MODEL(sentence)
        subject_locators = [
            partial(locate_matching_token, tokens, 'text', self._SUBJ_SPACE_CHAR),
            *[
                partial(locate_matching_token, tokens, 'dep_', subj_dependency)
                for subj_dependency in self._SUBJ_DEPENDENCIES
            ]
        ]

        for subject_locator in subject_locators:
            possible_subject = subject_locator()
            if possible_subject:
                return possible_subject.text
