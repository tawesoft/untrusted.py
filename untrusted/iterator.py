import untrusted
import collections.abc


class iterator(collections.abc.Iterable):

    _keyType = TypeError # NA
    _valueType = untrusted.string

    def __init__(self, value, valueType=None):
        """value may be any iterable, e.g. a container, sequence, generator,
           or iterable."""

        if valueType is not None:
            assert isinstance(valueType, type)
            self._valueType = valueType

        self._value = value
   
    def __iter__(self):
        for x in self._value:
            yield self._valueType(x)

    def __repr__(self):
        return "<untrusted.iterator of type %s>" % repr(self._valueType)


Iterator = iterator


def iteratorOf(valueType):
    """Dynamically creates a new iterator type for use in the valueType argument
       of any untrusted iterator/collection constructor."""

    assert isinstance(valueType, type), "iteratorOf expects a type, not a value"
    return type('iterableOf.'+valueType.__module__+'.'+valueType.__name__, (iterator,),{"_valueType": valueType})
    

