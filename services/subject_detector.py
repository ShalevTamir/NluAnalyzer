import spacy
from spacy.tokens.token import Token


class SubjectDetector:
    SUBJ_DEPENDENCIES = ["subj","ROOT"]
    SUBJ_TRAIL_DEPENDENCIES = ["compound","mod"]
    def __init__(self):
        self.model = spacy.load('en_core_web_sm')

    def __find_token(self, lst_tokens, token_dependency) -> Token:
        for token in lst_tokens:
            if token_dependency in token.dep_:
                return token
    def __find_matching_token(self, lst_tokens, dependencies_to_match):
        for subject_dependency in dependencies_to_match:
            potential_partial_subject = self.__find_token(lst_tokens,subject_dependency)
            if potential_partial_subject:
                return potential_partial_subject



    def detect(self, sentence: str):
        doc = self.model(sentence)
        partial_subject: Token = self.__find_matching_token(doc,self.SUBJ_DEPENDENCIES)
        if partial_subject is None:
            return None
        complete_subject = [node.text
                            for node in partial_subject.subtree
                            if self.__find_matching_token([node], self.SUBJ_TRAIL_DEPENDENCIES) is not None] + \
                           [partial_subject.text]

        return ' '.join(complete_subject)
