from spacy.tokens.token import Token
from definitions import SPACY_MODEL
from services.utils.spacy_utils import find_dependencies


class SubjectDetector:
    _SUBJ_DEPENDENCIES = ["subj", "ROOT"]
    _SUBJ_TRAIL_DEPENDENCIES = ["compound", "mod"]
    _NUMBER_POS_TAG = "NUM"
    _SUBJ_SPACE_CHAR = '_'

    def detect(self, sentence: str):
        doc = SPACY_MODEL(sentence)

        for token in doc:
            if self._SUBJ_SPACE_CHAR in token.text:
                return token.text

        root_subjects = find_dependencies(doc, self._SUBJ_DEPENDENCIES)
        root_subject: Token = next(root_subjects) if root_subjects else None
        complete_subject = []
        if root_subject is not None:
            complete_subject.append(root_subject.text)
            return ' '.join(complete_subject)
