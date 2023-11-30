from typing import NamedTuple

from spacy.tokens import Token

from flask_app.nlu_pkg.models.enums.duration_type import DurationType
from flask_app.nlu_pkg.models.enums.noun_type import NounType


class DurationUnit(NamedTuple):
    duration_token: Token
    duration_type: DurationType
    noun_type: NounType
