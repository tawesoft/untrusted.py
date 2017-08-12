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

assert same(untrusted.normal(unnormalised), untrusted.normal(normalised))

assert same(normalised, untrusted.normal(unnormalised) / html.escape)
assert same(normalised, untrusted.normal(normalised) / html.escape)

assert not same(unnormalised, untrusted.normal(unnormalised) / html.escape)

# the internal representation is in NFD
# this an implementation detail that does not have to be true
# but let's test manually that this is still true
# because we're unlikely to want to change this by accident
assert same(unnormalised, untrusted.normal(unnormalised).value)
assert same(unnormalised, untrusted.normal(normalised).value)


# assert that for `untrusted.normalised(x) / escapefun`, escapefun sees the
# NFD form, and a returned value in NFD is then converted to NFC automatically

def myescape(s):
    assert same(s, u'\u0061\u0301')
    return s

assert same(normalised, untrusted.normal(unnormalised) / myescape)
assert same(normalised, untrusted.normal(normalised) / myescape)




# test tainting works as you'd expect still

a = untrusted.normal(unnormalised)
b = untrusted.normal(normalised)

_a = ' ' + a
_b = ' ' + b
assert type(_a) is untrusted.normal
assert type(_b) is untrusted.normal
assert same(untrusted.normal(' ' + u'\u00e1'), ' ' + a)
assert same(untrusted.normal(' ' + u'\u00e1'), ' ' + b)
assert same(_a, _b)

a_ = a + ' '
b_ = b + ' '
assert type(a_) is untrusted.normal
assert type(b_) is untrusted.normal
assert same(untrusted.normal(u'\u00e1'+' '), a + ' ')
assert same(untrusted.normal(u'\u00e1'+' '), b + ' ')
assert same(a_, b_)

baba = b + a + b + a
assert type(baba) is untrusted.normal
assert same(untrusted.normal(u'\u00e1\u0061\u0301\u00e1\u0061\u0301'), baba)


# test subclassing works too

class mynormal(untrusted.normal):
    pass

unnormalised = u'\u0061\u0301'
normalised   = u'\u00e1'

a = mynormal(unnormalised)
b = mynormal(normalised)

assert same(a, b)

assert same(normalised, mynormal(unnormalised) / html.escape)
assert same(normalised, mynormal(normalised) / html.escape)

assert not same(unnormalised, mynormal(unnormalised) / html.escape)

a = mynormal(unnormalised)
b = mynormal(normalised)

_a = ' ' + a
_b = ' ' + b
assert type(_a) is mynormal
assert type(_b) is mynormal
assert same(mynormal(' ' + u'\u00e1'), ' ' + a)
assert same(mynormal(' ' + u'\u00e1'), ' ' + b)
assert same(_a, _b)

a_ = a + ' '
b_ = b + ' '
assert type(a_) is mynormal
assert type(b_) is mynormal
assert same(mynormal(u'\u00e1'+' '), a + ' ')
assert same(mynormal(u'\u00e1'+' '), b + ' ')
assert same(a_, b_)

baba = b + a + b + a
assert type(baba) is mynormal
assert same(mynormal(u'\u00e1\u0061\u0301\u00e1\u0061\u0301'), baba)




