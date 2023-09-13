import spacy


class SubjectDetector:
    SUBJ_DEPENDENCIES = ["subj", "ROOT"]

    def __init__(self):
        self.model = spacy.load('en_core_web_sm')

    def __find_token(self, lst_tokens, token_dependency):
        for token in lst_tokens:
            if token_dependency in token.dep_:
                return token

    def detect(self, sentence: str):
        doc = self.model(sentence)
        for dependency in self.SUBJ_DEPENDENCIES:
            potential_subj = self.__find_token(doc, dependency)
            if potential_subj:
                return potential_subj.text
