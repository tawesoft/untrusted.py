import untrusted
import collections.abc


class sequence(collections.abc.Iterable):

    _valueType = untrusted.string

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

    def __bool__(self):
        return True if self.obj else False
    
    def __len__(self):
        return len(self.obj)

    @property
    def obj(self):
        """Read only access to the underlying object."""
        return self._value


def sequenceOf(valueType):
    """Dynamically creates a new sequence type for use in the valueType argument
       of the sequence constructor."""

    assert isinstance(valueType, type), "sequenceOf expects a type, not a value"
    return type('sequenceOf.'+valueType.__module__+'.'+valueType.__name__, (sequence,),{"_valueType": valueType})
    

