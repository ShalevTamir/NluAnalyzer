from typing import NamedTuple

from spacy.tokens import Token

from ..enums.duration_type import DurationType
from ..enums.noun_type import NounType


class DurationUnit(NamedTuple):
    duration_token: Token
    duration_type: DurationType
    noun_type: NounType
