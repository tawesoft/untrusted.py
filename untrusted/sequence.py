import untrusted
import collections.abc


class sequence(collections.abc.Iterable):

    _valueType = untrusted.string

    def __init__(self, value, valueType=None):
        """value may be a container or an iterator object itself"""

        if valueType is not None:
            assert isinstance(valueType, type)
            self._valueType = valueType

        self._value = value
   
    def __iter__(self):
        return untrusted.iterable(self._value)

    def __repr__(self):
        return "<untrusted.sequence of type %s>" % repr(self._valueType)


def sequenceOf(valueType):
    """Dynamically creates a new sequence subclass with a specific valueType"""

    assert isinstance(valueType, type)
    return type('sequenceOf.'+valueType.__module__+'.'+valueType.__name__, (sequence,),{"_valueType": valueType})
    

