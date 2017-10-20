def is_lambda(object_type):
    a_lambda = lambda: 0  # noqa
    return isinstance(object_type, type(a_lambda)) and object_type.__name__ == a_lambda.__name__
