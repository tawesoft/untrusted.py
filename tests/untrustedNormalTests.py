# The untrusted.normal does unicode normalisation

import untrusted
import html


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


unnormalised = u'\u0061\u0301'
normalised   = u'\u00e1'

assert not same(normalised, unnormalised)

a = untrusted.normal(unnormalised)
b = untrusted.normal(normalised)

assert same(untrusted.normal(unnormalised), untrusted.normal(normalised))

assert same(unnormalised, untrusted.normal(normalised).value)

assert same(normalised, untrusted.normal(unnormalised) / html.escape)
assert same(normalised, untrusted.normal(normalised) / html.escape)
