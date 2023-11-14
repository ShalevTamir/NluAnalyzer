import os
from spacy import Language
import spacy

from spacy.lang.en import stop_words

from flask_app.nlu_pkg.models.definitions.file_def import ROOT_DIR, DOCUMENTS_DIRECTORY_NAME
from flask_app.nlu_pkg.services.decorators.number_validation import validate_numbers_spacy

SPACY_MODEL = spacy.load("en_core_web_sm")
Language.__call__ = validate_numbers_spacy(Language.__call__)
NER_MODEL = spacy.load(os.path.join(ROOT_DIR, DOCUMENTS_DIRECTORY_NAME, "ner_detection_model"))
SPAN_SUBJECT_ATTR = 'subject'
STOP_WORDS = stop_words.STOP_WORDS - {'amount'}

# DEPENDENCIES
NEGATION_DEP = 'neg'
COORDINATION_DEP = 'cc'
CONJUNCTION_DEP = 'conj'
ADVERBIAL_MODIFIER_DEP = 'advmod'
QUANTITY_MODIFIER_DEP = 'quantmod'
SUBJECT_DEP = 'nsubj'
ROOT_DEP = 'ROOT'
DIRECT_OBJECT_DEP = 'dobj'
COMPOUND_DEP = 'compound'

# POS TAGS
NUMERICAL_POS_TAG = "NUM"
ADVERB_POS_TAG = "ADV"
ADJECTIVE_POS_TAG = "ADJ"
ADPOSITION_POS_TAG = 'ADP'
VERB_POS_TAG = 'VERB'
NOUN_POS_TAG = 'NOUN'
COORDINATING_CONJUNCTION_POS_TAG = 'CCONJ'
CONJUNCTION_POS_TAG = 'CONJ'
SUBORDINATING_CONJUNCTION_POS_TAG = 'SCONJ'
PUNCTUATION_POS_TAG = 'PUNCT'
PARTICLE_POS_TAG = 'PART'
SYMBOL_POS_TAG = 'SYM'
PRONOUN_POS_TAG = 'PRON'
PART_POS_TAG = 'PART'
UNKNOWN_POS_TAG = ''

# ATTRIBUTES
SPACY_DEP_ATTR = 'dep_'
SPACY_POS_ATTR = 'pos_'
SPACY_TEXT_ATTR = 'text'

# PATTERNS
PATTERN_POS_ATTR = 'POS'
PATTERN_DEP_ATTR = 'DEP'
PATTERN_OP_ATTR = 'OP'
PATTERN_IN_ATTR = 'IN'
PATTERN_NOT_IN_ATTR = 'NOT_IN'
PATTERN_TEXT_ATTR = 'TEXT'

DEFAULT_PATTERN_NAME = ""
