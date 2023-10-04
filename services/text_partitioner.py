import spacy
from services.utils.spacy_utils import matching_tokens


class TextPartitioner:
    SUBJ_DEPENDENCY = "subj"

    def __init__(self):
        self.__model = spacy.load('en_core_web_sm')

    def extract_sentences(self, text) -> list[str]:
        doc = self.__model(text)
        first_subject = True

        for index in range(len(doc)):
            if self.SUBJ_DEPENDENCY in doc[index].dep_:
                if first_subject:
                    first_subject = False
                else:
                    pass

        return [text]




