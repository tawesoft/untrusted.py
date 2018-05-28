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

Strategies for sanitizing, escaping, normalising or validating input are out of
scope for this module.


## Status

This module should be suitable for production use, with the following caveats:

* *TODO* `untrusted.sequence` type is missing tests and may be incomplete
* *TODO* `untrusted.mapping` type is missing tests and may be incomplete
* *TODO* `unstrusted.<*>Of` is not fully tested
* *TODO* statically-verifiable type safety has not been tested

Any code with security considerations deserves the highest standards of
scrutiny. Please exercise your judgement before using this module.


## Quickstart

Tested for Python >= 3.4, but earlier versions may work.


### Get Untrusted

    sudo pip3 install untrusted --upgrade

(If you only have python3 installed, you may need only `pip` - not `pip3`)

### Try it!

```python
import html # for html.escape
import untrusted

line = untrusted.string(input("Enter some text, HTML will be escaped: "))

try:
    # You're not allowed to print an untrusted.string!
    # This raises a TypeError!
    print("<b>You typed:</b> " + line)
except TypeError:
    pass # Expected

# Safely escape the HTML!
print("<b>You typed:</b> " + line / html.escape)

# / is overloaded as shorthand for:
# print("<b>You typed:</b> " + line.escape(html.escape))
```


## Overview

### The `untrusted.string` type

* Looks and feels like a `str` type, but can't be output without escaping
* Seamlessly interoperable with native `str` types
* Mixed usage of native `str` and `untrusted.string` taints `str`
values/promotes them to `untrusted.string` types.

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
    fullName.encode('utf8') # also raises TypeError
except TypeError:
    print("We caught an error, as expected!")

# instead, you are forced to explicitly escape your string somehow
print("<b>Escaped output:</b> " + fullName.escape(html.escape)) # prints safe HTML!
print("<b>Escaped output:</b> " + fullName / html.escape) # use this easy shorthand!
```

See `untrustedStringExample.py` for composing multiple escape functions,
passing arguments to escape functions, etc.


### Untrusted collection types

This module provides types to lazily wrap collections of untrusted values.
The values are wrapped with an appropriate `untrusted.*` type when accessed.


#### `untrusted.iterator`

* This is a [view](https://docs.python.org/3/library/stdtypes.html#dictionary-view-objects)
over any iterable or generator yielding untrusted values.
* It only yields values wrapped by an `untrusted.*` type
* Usually this is an `untrusted.string` but it can also be an iterator over
untrusted collections

Example:

```python
import html # for html.escape
import untrusted

it = untrusted.iterator(open("example.txt"))

for i, s in enumerate(it):
    print("Line %d: %s" % (i, s.escape(html.escape).strip()))
```

See `examples/untrustedIteratorExample.py` for an untrusted nested list
(e.g. an `untrusted.iterator` of `untrusted.iterator` of `untrusted.string`).


#### `untrusted.sequence`

* This is a [view](https://docs.python.org/3/library/stdtypes.html#dictionary-view-objects)
over any `list`-like object containing untrusted values.
* All accessed values are wrapped by an `untrusted.*` type
* Usually this is an `untrusted.string` but it can also be an iterator over
untrusted collections

Example:

```python
import html # for html.escape
import untrusted

# list of strings from an untrusted source
animals = ["cat", "dog", "monkey", "elephant", "<big>mouse</big>"]

untrustedAnimalList = untrusted.sequence(animals)

assert "cat" in untrustedAnimalList
``` 


#### `untrusted.mapping`

* This is a [view](https://docs.python.org/3/library/stdtypes.html#dictionary-view-objects)
over any `dict`-like object mapping trusted or untrusted keys to untrusted values.
* All accessed values, and optionally keys, are wrapped by an `untrusted.*` type.
* Usually this is a mapping `str` -> `untrusted.string`, but it could
also be a mapping `unstrusted.string` -> `untrusted.string`, or a mapping
to an untrusted collection.

Example:

```python3
import html # for html.escape
import untrusted

user = untrusted.mapping({
    'username': 'example-username<b>hack attempt</b>',
    'password': 'example-password',
})

try:
    print(user.get("username")) 
except TypeError:
    print("Caught the error we expected!")

print(user.get("username", "default-username") / html.escape)
```

Example:

```python3
import html # for html.escape
import untrusted

untrustedType = untrusted.mappingOf(untrusted.string, untrusted.string)

args = untrustedType({'animal': 'cat', '<b>hack</b>': 'attempt'})

for k,v in args.items():
    print("%s: %s" % (k / html.escape, v / html.escape))
```


#### Custom and Nested Containers

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


## Usage

### untrusted.string

Supports most native `str` methods, but may possibly
have different return types.

### untrusted.string.value property

The underlying value - always a non-None instance of `str`.

### untrusted.string()

`untrusted.string(s)`

Constructs a `untrusted.string` object, where `s` is a non-None instance
of `str` or `untrusted.string`.

In the case of an `untrusted.string` being constructed with an
`untrusted.string` argument, the new value is only wrapped once. Escaping
it will give a `str`, not an `untrusted.string`.

#### untrusted.string.escape()

`untrusted.string.escape(escape_function, [*args, **kwargs]) -> str`

Applies the `escape_function`, a function `str -> str` that escapes
a string and returns it, with optional arguments and keyword arguments.

#### untrusted.string.valid()

`untrusted.string.valid(valid_function, [*args, **kwargs]) -> bool`

Applies the `valid_function`, a function `str -> bool`, that checks
a string and returns True or False, with optional arguments and
keyword arguments.

#### untrusted.string.validate()

`untrusted.string.valid(validate_function, [*args, **kwargs]) -> any`

Applies the `valid_function`, a function `str -> any`, that checks
a string and returns any value (e.g. a list of reasons why a string did not
validate), with optional arguments and keyword arguments.


#### Overload: `untrusted.string / escape_expr`

For some escape expression, `untrusted.string("value") / escape_expr -> str`

An `escape_expr` here is either a function `str -> str` that escapes a string,
or a 3-tuple `(escape_function, args, kwargs_dict)`, for example:

```python
import html # for html.escape
import untrusted

myString = untrusted.string("<b>Exam\"ple</b>")
myEscape = (html.escape, [], {'quote': False})

print(myString / html.escape)
print(myString / myEscape)
```


### untrusted.\<collection\>

Where `collection` is one of `iterator`, `sequence` (list-like),
`mapping` (dict-like), or a user-constructed custom type.

Supports most native collection methods, but may possibly
have different return types.

Each collection is aware of its **Value Type** (default
`untrusted.string`).

Mappings are also aware of their **Key Type** (default `str`)


### untrusted.\<collection\>.value property

The underlying value - always a non-None object that is
an instance of the collection's Value Type.

### untrusted.\<collection\> Type Constructors

Create an iterator type using `untrusted.iteratorOf(type)`.

Create a sequence type using `untrusted.sequenceOf(type)`.

Create a mapping type using `untrusted.sequenceOf(keyType, valueType)`.

These definitions are recursive.

For example:

```python
import untrusted

itType = untrusted.iteratorOf(untrusted.iteratorOf(untrusted.string))
seqType = untrusted.sequenceOf(itType)
mappingType = untrusted.mappingOf(untrusted.string, seqType)

someDict = {}
myMapping = mappingType(someDict)

# or, as a less readable one-liner
myMapping = untrusted.mappingOf(untrusted.string, seqType)(someDict)
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

    Copyright © 2017 - 2018 Ben Golightly <ben@tawesoft.co.uk>
    Copyright © 2017 - 2018 Tawesoft Ltd <opensource@tawesoft.co.uk>

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

