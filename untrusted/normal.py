import unicodedata
import untrusted
import untrusted.util


# here's a string class that normalises the Unicode to NFD on init and NFC on exit

class normal(untrusted.string):
    def __init__(self, value):
        if isinstance(value, untrusted.string):
            value = value.value
        if not isinstance(value, str):
            raise TypeError("Initialiser for an untrusted string must be an instance of str or untrusted.string")

        self._value = unicodedata.normalize("NFD", value)

    def __reversed__(self):
        # Naive Python reversed(str) often gives a nonsensical result anyway,
        # no matter the normalisation format.
        raise NotImplemented

    def escape(self, fn, *args, **kwargs) -> str:
        result = fn(unicodedata.normalize("NFC", self.value), *args, **kwargs)
        assert isinstance(result, str)
        return result


Normal=normal
