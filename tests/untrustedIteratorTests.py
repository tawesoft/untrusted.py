# This file contains fairly exhaustive tests of almost all the methods
# supported by a Python iterator, and tests that `untrusted.iterator` type:
# * correctly supports the same methods
# * accepts `str` and/or `untrusted.string` arguments interchangeably
# * never returns `str` or any iterable of `str`, only an
#   appropriate `untrusted.*` type.
# Also tests that subclassed instances of untrusted.iterator works too

import untrusted

# https://docs.python.org/3.4/library/stdtypes.html#typeiter


def same(a, b):
    if type(a) != type(b):
        return False
    if isinstance(a, untrusted.string):
        a = a.value
    if isinstance(b, untrusted.string):
        b = b.value
    if a != b:
        return False
    return True



def animalGenerator():
    yield "cat"
    yield "dog"
    yield "mouse"

for i in animalGenerator():
    assert i in ("cat", "dog", "mouse")
    assert isinstance(i, str)

for i in untrusted.iterator(animalGenerator()):
    assert i in ("cat", "dog", "mouse")
    assert isinstance(i, untrusted.string)

it = untrusted.iterator(animalGenerator())

# an iterator always returns itself
assert iter(it) is it

assert same(untrusted.string("cat"), next(it))
assert same(untrusted.string("dog"), next(it))
assert same(untrusted.string("mouse"), next(it))

try:
    _ = next(it)
    raise AssertionError
except StopIteration:
    pass # expected

