import spacy
from spacy import displacy
from spacy.tokens.token import Token

from services.classification.preprocessing.preprocessor import preprocess_sentence
from services.utils.spacy_utils import matching_tokens, token_match


class SubjectDetector:
    SUBJ_DEPENDENCIES = ["subj", "ROOT"]
    SUBJ_TRAIL_DEPENDENCIES = ["compound", "mod"]
    NUMBER_POS_TAG = "NUM"

    def __init__(self):
        self.model = spacy.load('en_core_web_sm')

    def detect(self, sentence: str):
        doc = self.model(sentence)

        for token in doc:
            if '_' in token.text:
                return token.text
            
        root_subjects = matching_tokens(doc, self.SUBJ_DEPENDENCIES)
        root_subject: Token = next(root_subjects) if root_subjects else None
        complete_subject = []
        if root_subject is None:
            return None
        # for node in root_subject.lefts:
        #     if token_match(node.dep_, self.SUBJ_TRAIL_DEPENDENCIES) \
        #             and not token_match(node.pos_, [self.NUMBER_POS_TAG]):
        #         complete_subject.append(node.text)
        complete_subject.append(root_subject.text)

        return ' '.join(complete_subject)
