import collections.abc
import string as stringmodule
import untrusted
import untrusted.util


class _incompleteStringType:
    _keyType = TypeError # NA
    _valueType = None # set later (circular reference)

    # when calling `repr(untrusted.string)`, unicode is escaped and converted
    # to ASCII. Then all symbols not in `_repr_whitelist` are replaced with
    # `_repr_replace`. Values longer than _repr_maxlen are truncated.
    _repr_whitelist = stringmodule.ascii_letters + stringmodule.digits + ' '
    _repr_replace = '.'
    _repr_maxlen = 128 # must be >= 3

    _cast_error = "Implicit cast to/of untrusted.string is not allowed"

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
        '__contains__',
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
        '__mul__',
        '__rmul__',
        '__getitem__',
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
        '__reversed__': untrusted.util._to_untrusted_iterator,
        'partition':    untrusted.util._to_untrusted_tuple_of_strings, # returns a 3-tuple
        'rpartition':   untrusted.util._to_untrusted_tuple_of_strings, # returns a 3-tuple
        'split':        untrusted.util._to_untrusted_list,
        'splitlines':   untrusted.util._to_untrusted_list,
    }

    # disallowed: encode
    # not yet considered: maketrans, translate

    def __getattr__(self, name):
        return untrusted.util._wrapped_method(self, name)

    def __init__(self, value):
        assert value is not None
        assert isinstance(value, str), "Expected str. got %s" % repr(type(value))
        self._value = value

    def __radd__(self, *args):
        # underlying str doesn't implement __radd__ for us to wrap
        other, *_ = untrusted.util._wrap_args(*args)
        return self._valueType(other + self.value)
    
    def __reversed__(self):
        # underlying str doesn't have __reversed__ for us to wrap
        return untrusted.iterator(reversed(self.value))

    def __str__(self):
        raise TypeError(self._cast_error)

    def __repr__(self):
        # in case a repr gets printed by accident, ensure even the preview
        # is escaped
        value = self.value.encode('unicode_escape').decode('latin-1')
        value = ''.join(map(lambda x: x if x in self._repr_whitelist else self._repr_replace, value))

        if len(value) > self._repr_maxlen:
            value = value[self._repr_maxlen - 3] + "..."

        if (value != self.value):
            return "<untrusted.string: (escaped/sanitised/truncated) %s>" % repr(value)
        else:
            return "<untrusted.string: %s>" % repr(value)

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


# we dynamically create the actual untrusted.string class from the above class
# with some magic to let us easily passthrough magic methods that are otherwise
# not picked up when operator overloading

string = type('string', (_incompleteStringType,), untrusted.util._createMagicPassthroughBindings(
    ["add", "contains", "bool", "eq", "gt", "gte", "getitem", "len", "lt", "lte", "mul", "neq", "rmul"]
))
string._valueType = string



