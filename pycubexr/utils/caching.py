import sys

if sys.version_info >= (3, 8):
    import functools

    cached_property = functools.cached_property
else:
    class cached_property(object):
        """
        A property that is cached for later retrieval.
        """

        def __init__(self, func):
            self.func = func

        def __get__(self, obj, cls):
            if obj is None:
                return self

            value = self.func(obj)
            obj.__dict__[self.func.__name__] = value
            return value
