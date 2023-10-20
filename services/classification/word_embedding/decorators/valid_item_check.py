def check_validity(validation_func):
    def decorator(func_to_execute):
        def wrapper(*args, **kwargs):
            if validation_func(*args, **kwargs):
                return func_to_execute(*args, **kwargs)
            else:
                raise ValueError()
        return wrapper
    return decorator

