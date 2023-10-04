from functools import wraps
from flask import request, abort
import inspect


def includes_body_params(func):
    @wraps(func)
    def decorated_function():
        body_params = request.json
        func_args = inspect.getfullargspec(func).args
        for args in func_args:
            if args not in request.json:
                abort(400, f'Missing argument {args}')
        return func(**body_params)

    return decorated_function

