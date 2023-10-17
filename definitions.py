import os

import spacy

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DOCUMENTS_DIRECTORY_NAME = "documents"

ERROR_MSG = "Unable to parse sentence"
INVALID_SENT = "Invalid sentence"
COMPARATIVE_ADJECTIVE_POS_TAG = "JJR"
NUMERICAL_POS_TAG = "CD"
ADJECTIVE_OR_NUMERICAL_POS_TAG = "JJ"
CONJUNCTION_POS_TAG = "IN"
FIND_NUMBERS_REG = r'-?\d+(?:\.\d+)?'
PARAMETER_NUMBERS_COUNT = 1
RANGE_NUMBERS_COUNT = 2

SPACY_MODEL = spacy.load("en_core_web_sm")
