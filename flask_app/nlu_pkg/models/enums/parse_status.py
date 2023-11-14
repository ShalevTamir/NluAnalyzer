from enum import Enum


class ParseStatus(Enum):
    SUCCESSFUL = 0
    INVALID_RANGE = 1
    UNABLE_TO_PARSE = 2
