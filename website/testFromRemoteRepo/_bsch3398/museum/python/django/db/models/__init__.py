# Admin stages.
ADD, CHANGE, BOTH = 1, 2, 3


def permalink(func):
    """
    Decorator that calls urlresolvers.reverse() to return a URL using
    parameters returned by the decorated function "func".

    "func" should be a function that returns a tuple in one of the
    following formats:
        (viewname, viewargs)
        (viewname, viewargs, viewkwargs)
    """
    from django.core.urlresolvers import reverse

    def inner(*args, **kwargs):
        bits = func(*args, **kwargs)
        return reverse(bits[0], None, *bits[1:3])

    return inner
