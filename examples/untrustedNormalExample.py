import untrusted
import html

unnormalised = u'\u0061\u0301' # á
normalised   = u'\u00e1'       # also á

assert unnormalised != normalised
assert untrusted.normal(unnormalised) == untrusted.normal(normalised)
assert normalised == untrusted.normal(unnormalised) / html.escape
