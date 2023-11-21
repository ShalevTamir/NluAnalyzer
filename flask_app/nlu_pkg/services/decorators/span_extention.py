from functools import wraps
from typing import Callable

from spacy.tokens import Span


def custom_getitem(default_getitem: Callable):
    @wraps(default_getitem)
    def wrapper(self: Span, index):
        if isinstance(index, int):
            index = _adjust_index(self, index)
        elif isinstance(index, slice):
            index = slice(
                _adjust_index(self, index.start),
                _adjust_index(self, index.stop),
                _adjust_index(self, index.step)
            )
        return default_getitem(index)

    return wrapper


def _adjust_index(span: Span, index: int | None):
    return index if index is None else span.start - index
