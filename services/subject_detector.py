import spacy
from spacy import displacy
from spacy.tokens.token import Token

from services.classification.preprocessing.preprocessor import preprocess_text


class SubjectDetector:
    SUBJ_DEPENDENCIES = ["subj", "ROOT"]
    SUBJ_TRAIL_DEPENDENCIES = ["compound", "mod"]
    NUMBER_POS_TAG = "NUM"

    def __init__(self):
        self.model = spacy.load('en_core_web_sm')

    def __is_token_match(self, token_property: str, dependencies_to_match: list[str]) -> bool:
        for dependency in dependencies_to_match:
            if dependency in token_property:
                return True
        return False

    def __extract_matching_tokens(self, lst_token, dependencies_to_match: list[str], pos_tags_to_exclude=None) -> Token:

        for token in lst_token:
            if self.__is_token_match(token.dep_, dependencies_to_match) and \
                    not self.__is_token_match(token.pos_,
                                              pos_tags_to_exclude if pos_tags_to_exclude is not None else []):
                return token

    def detect(self, sentence: str):
        sentence = preprocess_text(sentence)
        doc = self.model(sentence)
        root_subject: Token = self.__extract_matching_tokens(doc, self.SUBJ_DEPENDENCIES)
        complete_subject = []
        if root_subject is None:
            return None
        for node in root_subject.lefts:
            node = self.__extract_matching_tokens([node], self.SUBJ_TRAIL_DEPENDENCIES, [self.NUMBER_POS_TAG])
            if node:
                complete_subject.append(node.text)
        complete_subject.append(root_subject.text)

        return ' '.join(complete_subject)
