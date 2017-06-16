import untrusted
import collections.abc


class string:
    _cast_error = "Implicit cast of untrusted string input is not allowed"

    @staticmethod
    def _to_untrusted_list(xs): return untrusted.sequence(xs)
    @staticmethod
    def _to_untrusted_tuple(xs): return tuple(map(string, xs))

    # whitelist of methods to wrap that return a simple value e.g. boolean
    _safe_methods = set([
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

    # disallowed: encode, join
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
            raise TypeError(self._cast_error)

    def __init__(self, value):
        assert value is not None
        assert isinstance(value, str)
        self._value = value
    
    def __eq__(self, other):
        if isinstance(other, string):
            return (self._value == other.value)
        elif isinstance(other, str):
            return (self._value == other)
        else:
            raise TypeError(self._cast_error)
    
    def __add__(self, other):
        if isinstance(other, string):
            return string(self._value + other.value)
        elif isinstance(other, str):
            return string(self._value + other)
        else:
            raise TypeError(self._cast_error)
    
    def __radd__(self, other):
        if type(other) is string:
            return string(other.value + self._value)
        elif isinstance(other, str):
            return string(other + self._value)
        else:
            raise TypeError(self._cast_error)

    def __bool__(self):
        return True if self._value else False
    
    def __len__(self):
        return len(self._value)
    
    def __str__(self):
        raise TypeError(self.__class__._cast_error)

    def __repr__(self):
        return "<untrusted.string: %s>" % repr(self._value)

    @property
    def value(self):
        """Read only access to the raw `str` value."""
        return self._value

    def escape(self, fn, *args, **kwargs):
        result = fn(self._value, *args, **kwargs)
        assert isinstance(result, str)
        return result

    def validate(self, fn, *args, **kwargs):
        result = fn(self._value, *args, **kwargs)
        assert isinstance(result, bool)
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


