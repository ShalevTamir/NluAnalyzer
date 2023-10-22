import os
import spacy
from spacy import Language

from services.decorators.number_validation import validate_numbers_spacy

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DOCUMENTS_DIRECTORY_NAME = "documents"
ERROR_MSG = "Unable to parse sentence"
INVALID_SENT = "Invalid sentence"
COMPARATIVE_ADJECTIVE_POS_TAG = "JJR"
NUMERICAL_POS_TAG_NLTK = "CD"
NUMERICAL_POS_TAG_SPACY = "NUM"
ADJECTIVE_OR_NUMERICAL_POS_TAG = "JJ"
CONJUNCTION_POS_TAG = "IN"
PARAMETER_NUMBERS_COUNT = 1
RANGE_NUMBERS_COUNT = 2
CONJUNCTION_DEP = 'cc'
NEGATION_DEP = 'neg'
SPACY_MODEL = spacy.load("en_core_web_sm")
Language.__call__ = validate_numbers_spacy(Language.__call__)
