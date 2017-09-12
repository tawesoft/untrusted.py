# Untrusted: safer Python with types for untrusted input

> The most common web application security weakness is the failure to properly
> validate input from the client or environment.

[OWASP, Data Validation](https://www.owasp.org/index.php/Data_Validation) (2 July 2017)

Failure to properly handle untrusted input leaves an application vulnerable to
[Code Injection attacks](https://www.owasp.org/index.php/Code_Injection), such
as [Cross Site Scripting (XSS)](https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)).
"Some form of visible tainting on input from the client or untrusted sources" is
one countermeasure recommended by OWASP, as part of a strategy of
[Defence in Depth](https://www.owasp.org/index.php/Defense_in_depth).

This Python module "taints" untrusted input by wrapping them in special types.
These types behave in most respects just like native Python types, but prevent
you from using their values accidentally. This provides not just "visible
tainting", but runtime guarantees and statically-verifiable type safety.

Strategies for sanitizing, escaping and validating input is out of scope
for this module.


## Status

This module should be suitable for production use, with the following caveats:

* *TODO* there isn't a versioned release on pip yet
* *TODO* `untrusted.sequence` type is missing tests and may be incomplete
* *TODO* `untrusted.mapping` type is missing tests and may be incomplete
* *TODO* `unstrusted.\<*\>Of` is not fully tested
* *TODO* statically-verifiable type safety has not been tested

Any code with security considerations deserves the highest standards of
scrutiny. Please exercise your judgement before using this module.


## Quickstart

Tested for Python >= 3.4, but earlier versions may work.


### Get Untrusted

TODO. For now, clone the repo.


### The `untrusted.string` type

* Looks like a `str`.
* Feels like a `str`.
* Definitely isn't a `str`.

**Example of handling untrusted HTML:**

```python
import html # for html.escape()
import untrusted

# example of a string that could be provided by an untrusted user
firstName = untrusted.string("Grace")
lastName = untrusted.string("<script>alert('hack attempt!');</script>")

# works seamlessly with native python strings
fullName = firstName + " " + lastName

# fullName was tainted and keeps the untrusted.string type
print(repr(fullName)) # <untrusted.string of length 46>

# the normal string methods still work as you would expect
fullName = fullName.title()

# but you can't accidentally use it where a `str` is expected
try:
    print(fullName) # raises TypeError - untrusted.string used as a `str`!
except TypeError:
    print("We caught an error, as expected!")

# instead, you are forced to explicitly escape your string somehow
print("<b>Escaped output:</b> " + fullName.escape(html.escape)) # prints safe HTML!
print("<b>Escaped output:</b> " + fullName / html.escape) # use this easy shorthand!
```


### The `untrusted.normal` type

* Like the `untrusted.string` type, but with automatic Unicode normalisation
so that [canonically equivalent](https://en.wikipedia.org/wiki/Unicode_equivalence)
strings compare equal.

```python
import untrusted
import html

unnormalised = u'\u0061\u0301' # á
normalised   = u'\u00e1'       # also á

assert unnormalised != normalised
assert untrusted.normal(unnormalised) == untrusted.normal(normalised)
assert normalised == untrusted.normal(unnormalised) / html.escape
```

Values are normalised to NFD internally on input and normalised to NFC on output.

The value is normalised to NFC *before* being passed as input to `html.escape`.


### Untrusted collection types

This module provides types to lazily wrap collections of untrusted values.
The values are wrapped with an appropriate `untrusted.*` type when accessed.

#### `untrusted.iterator`

This is a [view](https://docs.python.org/3/library/stdtypes.html#dictionary-view-objects)
over any iterable or generator yielding untrusted values.

* Looks like a native `iterator`.
* Feels like a native `iterator`.
* Only yields values wrapped by an `untrusted.*` type.

#### `untrusted.sequence`

This is a [view](https://docs.python.org/3/library/stdtypes.html#dictionary-view-objects)
over any `list`-like object containing untrusted values.

* Looks like a native `list`.
* Feels like a native `list`.
* All accessed values are wrapped by an `untrusted.*` type.

#### `untrusted.mapping`

This is a [view](https://docs.python.org/3/library/stdtypes.html#dictionary-view-objects)
over any `dict`-like object mapping trusted or untrusted keys to untrusted values.

* Looks like a native `dict`.
* Feels like a native `dict`.
* All accessed values, and optionally keys, are wrapped by an `untrusted.*` type.

#### Nested containers

Lazily nested containers are fully supported, too.

Use `untrusted.iteratorOf(valueType)`, `untrusted.sequenceOf(valueType)`, or
`untrusted.mappingOf(keyType, valueType)` to create a specific
container type.

Example:

```python
import html # for html.escape
import untrusted

people = [
    {
        'id':           'A101',
        'name.first':   'Grace',
        'name.last':    'Hopper',
        'name.other':   'Brewster Murray',
        'dob':          '1906-12-09',
    },
    {
        'id':           'A102',
        'name.first':   'Alan',
        'name.last':    'Turing',
        'name.other':   'Mathison',
        'dob':          '1912-06-23',
    },
    {
        'id':           'HACKER',
        'name.first':   'Robert\'); DROP TABLE Students;--',
        'name.last':    '£Hacker',
        'dob':          '<b>Potato</b>'
    },
]


# a list of dicts with trusted keys, but untrusted values
mappingType = untrusted.sequenceOf(untrusted.mapping)

# aka (setting defaults explicitly)
mappingType = untrusted.sequenceOf(untrusted.mappingOf(str, untrusted.string))


for person in mappingType(people):
    for key, value in person.items():
        print("    %s: %s" % (key, value.escape(html.escape)))
```   


## Notes of Caution

### Different contexts

Remember, just because you have used one method to escape an `untrusted.string`
into a `str`, it may not be safe in other contexts. For example, what's safe
for HTML might still be dangerous SQL. At the time user input is captured, it
may not be known in advance the context in which it is to be used - and
therefore it is not yet known what is the correct validation and escaping
strategy. It's best to delay the escaping until the final point of use -
keep a value as `untrusted.*` for as long as possible.

This module isn't a magic solution. It's a tool to be used wisely. Don't fall
into the trap of thinking about a value "it's a `str` now so it's completely
safe".


### Escaping vs validation

Just because a string can be escaped safely, it does not mean that it has been
validated as allowable input. For example, you might put a minimum limit on
a password. Or you might require that an input isn't a
[reserved filename](https://stackoverflow.com/questions/448438/windows-and-renaming-folders-the-con-issue).

Nice ways to do this are to use `unstruted.string.valid` method, which returns 
a boolean, `untrusted.string.validate` method, which returns any value (e.g.
this might be a list of reasons why the input didn't valdiate), or to throw
a `ValueError` from a function that both escapes and validates.


### Use the best tool for the job

Sometimes, you generate HTML yourself and escaping is something you need to do.

Sometimes, an interface *always* separates parameters from code, like most
modern SQL libraries. In this case the database driver will handle potentially
untrusted input better than you ever could hope to, and escaping it is the
wrong thing to do.

You might mark the input as untrusted for other reasons - e.g. to enforce a
maximum length on a search query, or because you need to validate it against
business logic.


### The untrusted collection types are views, not copies

Untrusted collection types, like `untrusted.sequence`, are
"[views](https://docs.python.org/3/library/stdtypes.html#dictionary-view-objects)"
over the underling object. If the underlying object changes, so does the object you
see through the untrusted collection type. In other words: its a reference
to the same object, not a copy. If that's not what you want, use the
[copy module](https://docs.python.org/3.4/library/copy.html).

This should hopefully be obvious and unsuprising behaviour, not at all unique
to this module, but it can trip people up.


## License

This is free software ([MIT license](https://www.tawesoft.co.uk/kb/article/mit-license-faq)).

    untrusted - write safer Python with special untrusted types

    Copyright © 2017 Ben Golightly <ben@tawesoft.co.uk>
    Copyright © 2017 Tawesoft Ltd <opensource@tawesoft.co.uk>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction,  including without limitation the rights
    to use,  copy, modify,  merge,  publish, distribute, sublicense,  and/or sell
    copies  of  the  Software,  and  to  permit persons  to whom  the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice  and this permission notice  shall be  included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED  "AS IS",  WITHOUT WARRANTY OF ANY KIND,  EXPRESS OR
    IMPLIED,  INCLUDING  BUT  NOT LIMITED TO THE WARRANTIES  OF  MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE  AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
    AUTHORS  OR COPYRIGHT HOLDERS  BE LIABLE  FOR ANY  CLAIM,  DAMAGES  OR  OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

