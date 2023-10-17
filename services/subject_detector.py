import spacy
from spacy import displacy
from spacy.tokens.token import Token

from definitions import SPACY_MODEL
from services.classification.preprocessing.preprocessor import preprocess_sentence
from services.utils.spacy_utils import find_dependencies, matches_dependency


class SubjectDetector:
    SUBJ_DEPENDENCIES = ["subj", "ROOT"]
    SUBJ_TRAIL_DEPENDENCIES = ["compound", "mod"]
    NUMBER_POS_TAG = "NUM"


    def detect(self, sentence: str):
        doc = SPACY_MODEL(sentence)

        for token in doc:
            if '_' in token.text:
                return token.text
            
        root_subjects = find_dependencies(doc, self.SUBJ_DEPENDENCIES)
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
