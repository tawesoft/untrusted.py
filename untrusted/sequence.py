import collections.abc
import untrusted
import untrusted.util


class _incompleteSequenceType(collections.abc.Container):

    _keyType = TypeError # NA
    _valueType = untrusted.string

    # whitelist of methods to wrap that return a simple value e.g. boolean
    _safe_methods = set([
        '__bool__',
        '__len__',
        '__length_hint__',
        '__setitem__',
        '__delitem__',
        '__contains__',
        'append',
        'extend',
        'insert',
        'remove',
        'pop',
        'clear',
        'index',
        'count',
        'sort',
        'reverse',
    ])

    # whitelist of methods to wrap that return e.g. a `str` value, or any value
    # that must be wrapped by the valueType
    _simple_wrapped_methods = set([
        "__missing__",
        "__getitem__"
    ])

    # whitelist of methods to wrap that return some complicated type, e.g. a
    # list of strings, and we want them to be all wrapped by an appropriate
    # untrusted type
    _complex_wrapped_methods = {
        '__reversed__': untrusted.util._to_untrusted_iterator,
        'copy':         untrusted.util._to_untrusted_list,
    }

    def __init__(self, value, valueType=None):
        """value may be a collection/generator/iterator etc."""

        if valueType is not None:
            assert isinstance(valueType, type)
            self._valueType = valueType

        self._value = value
   
    def __iter__(self):
        yield from untrusted.iterator(self.obj, valueType=self._valueType)

    def __repr__(self):
        return "<untrusted.sequence of type %s>" % repr(self._valueType)

    def __getattr__(self, name):
        return untrusted.util._wrapped_method(self, name)

    @property
    def obj(self): # matches the dictionary view .obj property
        """Read only access to the underlying object."""
        return self._value

    @property
    def value(self): # for symmetry with untrusted.string
        """Read only access to the underlying object."""
        return self._value


sequence = type('sequence', (_incompleteSequenceType,), untrusted.util._createMagicPassthroughBindings(
    ["bool", "contains", "delitem", "len", "length_hint", "missing", "getitem", "setitem", "reversed"]
))


def sequenceOf(valueType):
    """Dynamically creates a new sequence type for use in the valueType argument
       of any untrusted iterator/collection constructor."""

    assert isinstance(valueType, type), "sequenceOf expects a type, not a value"
    return type('sequenceOf.'+valueType.__module__+'.'+valueType.__name__, (sequence,),{"_valueType": valueType})
    

