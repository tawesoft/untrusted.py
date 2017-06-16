import collections.abc
import untrusted
import untrusted.util


class _incompleteStringType:
    _cast_error = "Implicit cast to/of untrusted.string is not allowed"

    @staticmethod
    def _to_untrusted_list(xs): return untrusted.sequence(xs)
    @staticmethod
    def _to_untrusted_tuple(xs): return tuple(map(string, xs))

    # whitelist of methods to wrap that return a simple value e.g. boolean
    _safe_methods = set([
        '__bool__',
        '__eq__',
        '__gt__',
        '__gte__',
        '__len__',
        '__lt__',
        '__lte__',
        '__neq__',
        'count',
        'endswith',
        'find',
        'index',
        'isalnum',
        'isalpha',
        'isdecimal',
        'isdigit',
        'isidentifier',
        'islower',
        'isnumeric',
        'isprintable',
        'isspace',
        'istitle',
        'isupper',
        'rfind',
        'rindex',
        'startswith',
    ])

    # whitelist of methods to wrap that return a `str` value
    _simple_wrapped_methods = set([
        '__add__',
        '__radd__',
        'capitalize',
        'casefold',
        'center',
        'expandtabs',
        'format',
        'format_map',
        'join',
        'ljust',
        'lower',
        'lstrip',
        'replace',
        'rstrip',
        'strip',
        'swapcase',
        'title',
        'upper',
        'zfill'
    ])

    # whitelist of methods to wrap that return some complicated type, e.g. a
    # list of strings, and we want them to be all wrapped by an appropriate
    # untrusted type
    _complex_wrapped_methods = {
        'partition':    _to_untrusted_tuple.__func__, # returns a 3-tuple
        'rpartition':   _to_untrusted_tuple.__func__, # returns a 3-tuple
        'split':        _to_untrusted_list.__func__,  # returns a untrusted.list
        'splitlines':   _to_untrusted_list.__func__  # returns a untrusted.list
    }

    # disallowed: encode
    # not yet considered: maketrans, translate

    def __getattr__(self, name):
        if name in self._safe_methods:
            return self._safe_method_wrapper(getattr(self.value, name))
        elif name in self._simple_wrapped_methods:
            return self._simple_method_wrapper(getattr(self.value, name))
        elif name in self._complex_wrapped_methods:
            result_wrapper = self._complex_wrapped_methods.get(name)
            return self._complex_method_wrapper(result_wrapper, getattr(self.value, name))
        else:
            raise TypeError("attribute %s not supported by untrusted.string" % repr(name))

    def __init__(self, value):
        assert value is not None
        assert isinstance(value, str), "Expected str. got %s" % repr(type(value))
        self._value = value

    def __radd__(self, *args):
        other, *_ = self._wrap_args(*args)
        return self.__class__(other + self.value)
    
    def __str__(self):
        raise TypeError(self._cast_error)

    def __repr__(self):
        return "<untrusted.string: %s>" % repr(self.value)

    @property
    def value(self):
        """Read only access to the raw `str` value."""
        return self._value

    def escape(self, fn, *args, **kwargs) -> str:
        result = fn(self.value, *args, **kwargs)
        assert isinstance(result, str)
        return result

    def valid(self, fn, *args, **kwargs) -> bool:
        result = fn(self.value, *args, **kwargs)
        assert isinstance(result, bool)
        return result

    def validate(self, fn, *args, **kwargs) -> any:
        result = fn(self.value, *args, **kwargs)
        return result


    @classmethod
    def _wrap_arg(cls, arg):
        if isinstance(arg, string):
            return arg.value
        elif isinstance(arg, str):
            return arg
        elif isinstance(arg, collections.abc.Mapping):
            return cls._wrap_kwargs(**arg)
        elif hasattr(arg, "__iter__"):
            return map(lambda x: cls._wrap_arg(x), arg)
        else:
            return arg

    @classmethod
    def _wrap_args(cls, *args):
        return map(cls._wrap_arg, args)

    @classmethod
    def _wrap_kwargs(cls, **kwargs):
        _kwargs = dict()

        for key, value in kwargs.items():
            _kwargs[key] = cls._wrap_arg(value)

        return _kwargs


    def _safe_method_wrapper(self, fn):
        '''For a method returning a safe value and taking any number of
           arguments, optionally accepting untrusted.string types in place of
           `str` arguments, return the result as normal.'''

        def wrapper(*args, **kwargs):
            _args, _kwargs = self._wrap_args(*args), self._wrap_kwargs(**kwargs)
            result = fn(*_args, **_kwargs)
            assert not isinstance(result, str)
            return result

        return wrapper


    def _simple_method_wrapper(self, fn):
        '''For a method returning a string value and taking any number of
           arguments, optionally accepting untrusted.string types in place of
           `str` arguments, return the result as an `untrusted.string`.'''

        def wrapper(*args, **kwargs):
            _args, _kwargs = self._wrap_args(*args), self._wrap_kwargs(**kwargs)
            result = fn(*_args, **_kwargs)
            return self.__class__(result)

        return wrapper


    def _complex_method_wrapper(self, result_wrapper, fn):
        '''For a method returning any type of value, and taking any number of
           arguments, optionally accepting untrusted.string types in place of
           `str` arguments, return the result as an appropriate
            `untrusted.*` type.'''

        def wrapper(*args, **kwargs):
            _args, _kwargs = self._wrap_args(*args), self._wrap_kwargs(**kwargs)
            result = fn(*_args, **_kwargs)
            return result_wrapper(result)

        return wrapper


# we dynamically create the actual untrusted.string class from the above class
# with some magic to let us easily passthrough magic methods that are otherwise
# not picked up when operator overloading

string = type('string', (_incompleteStringType,), untrusted.util._createMagicPassthroughBindings(
    ["add", "bool", "eq", "gt", "gte", "len", "lt", "lte", "neq"]
))



