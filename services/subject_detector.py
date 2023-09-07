import spacy


class SubjectDetector:
    def __init__(self):
        self.model = spacy.load('en_core_web_sm')

    def _find_token(self, lst_tokens, token_dependency):
        for token in lst_tokens:
            if token_dependency in token.dep_:
                return token

    def detect_param(self, sentence: str):
        doc = self.model(sentence)
        #TODO: change to const
        subj_dependencies = ["subj","ROOT"]
        for dependency in subj_dependencies:
            potential_subj = self._find_token(doc, dependency)
            if potential_subj:
                return potential_subj.text
