import spacy

from definitions import SPACY_MODEL
from services.utils.spacy_utils import find_dependencies


class TextPartitioner:
    _SUBJ_DEPENDENCY = "subj"

    def extract_sentences(self, text) -> list[str]:
        doc = SPACY_MODEL(text)
        first_subject = True

        for index in range(len(doc)):
            if self._SUBJ_DEPENDENCY in doc[index].dep_:
                if first_subject:
                    first_subject = False
                else:
                    pass

        return [text]




