import collections.abc
import untrusted
import untrusted.util


class _incompleteMappingType(collections.abc.Mapping):

    _keyType = str # or untrusted.string
    _valueType = untrusted.string

    # whitelist of methods to wrap that return a simple value e.g. boolean
    _safe_methods = set([
        '__bool__',
        '__len__',
        '__length_hint__',
        '__setitem__',
        '__delitem__',
        '__contains__',
        "clear",
        "update"
    ])

    # whitelist of methods to wrap that return e.g. a `str` value, or any value
    # that must be wrapped by the valueType
    _simple_wrapped_methods = set([
        "__missing__",
        "__getitem__",
        "get",
        "pop",
        "setdefault",
    ])

    # whitelist of methods to wrap that return some complicated type, e.g. a
    # list of strings, and we want them to be all wrapped by an appropriate
    # untrusted type
    _complex_wrapped_methods = {
        '__reversed__': untrusted.util._to_untrusted_iterator,
        'copy': untrusted.util._to_untrusted_mapping
    }

    def __init__(self, value, keyType=None, valueType=None):
        """value may be a collection/generator/iterator etc."""

        if keyType is not None:
            assert isinstance(keyType, type)
            self._keyType = keyType
        if valueType is not None:
            assert isinstance(valueType, type)
            self._valueType = valueType

        self._value = value
        self._keyIterator = untrusted.iteratorOf(self._keyType)
        self._valueIterator = untrusted.iteratorOf(self._valueType)

    def iter(self):
        return iter(self.keys())

    def items(self):
        return map(lambda x: (self._keyType(x[0]), self._valueType(x[1])), self.obj.items())

    def keys(self):
        return self._keyIterator(self.value.keys())
   
    def values(self):
        return self._valueIterator(self.value.values())

    def popitem(self):
        k, v = self.value.popitem()
        return (self._keyType(k), self_valueType(v))

    def __iter__(self):
        yield from untrusted.iterator(self.obj, valueType=self._valueType)

    def __repr__(self):
        return "<untrusted.mapping of type %s to type %s>" % (repr(self._keyType), repr(self._valueType))

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


mapping = type('mapping', (_incompleteMappingType,), untrusted.util._createMagicPassthroughBindings(
    ["bool", "contains", "delitem", "len", "length_hint", "missing", "getitem", "setitem", "reversed"]
))


def mappingOf(keyType, valueType):
    """Dynamically creates a new mapping type for use in the valueType argument
       of a untrusted iterator/collection constructor."""

    assert isinstance(keyType, type), "mappingOf expects a type for keyType, not a value"
    assert isinstance(valueType, type), "mappingOf expects a type for valueType, not a value"
    return type('mappingOf.'+keyType.__module__+'.'+keyType.__name__+
                ".to."+valueType.__module__+'.'+valueType.__name__,
        (mapping,),{"_keyType": keyType, "_valueType": valueType})
    

