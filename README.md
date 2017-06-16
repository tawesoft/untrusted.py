# untrusted.py

TODO not yet finished


**Write safer Python with special untrusted types.**

Tested for Python >= 3.4, but earlier versions may work.

## Quickstart

### Get Untrusted

    pip install untrusted

or

    pip3 install untrusted

or via the repo on GitHub


### The `untrusted.string` type

* Looks like a `str`.
* Feels like a `str`.
* Definitely isn't a `str`.

**Example of handling untrusted HTML:**


    import html # for html.escape()
    import untrusted

    # example of a string that could be provided by an untrusted user
    inputString = untrusted.string("<script>alert('hack attempt!');</script>")

    try:
        print(inputString) # raises TypeError - untrusted.string used as a `str`!
    except TypeError:
        print("Can't safely print(inputString)!")

    print("Escaped output: %s" % inputString.escape(html.escape)) # prints safe HTML!


**Example of handling untrusted shell input potentially containing [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code):**


    # Try it out:
    # echo -e "\033[0;31mHacker!" | python3 ./example.py

    import untrusted

    def strip_nonprintable(x):
        return ''.join(filter(lambda x: x.isprintable(), x))

    # prompt user for input
    print("What is your name?")
    name = untrusted.string(input())

    # combine it naturally with a native `str` - no error here yet!
    # It's only when you *use* the untrusted.string that the error occurs
    reply = "Hello " + name

    # This is because by combining an `untrusted.string` with a `str`, you
    # get an `untrusted.string` as a result.

    try:
        print(reply) # raises TypeError - untrusted.string used as a `str`!
    except TypeError:
        print("Can't safely print(reply)!")

    print("Escaped output: %s" % reply.escape(strip_nonprintable))


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
over any `dict`-like object mapping keys to values, containing untrusted values and,
optionally, even untrusted keys.

* Looks like a native `dict`.
* Feels like a native `dict`.
* All accessed values, and optionally keys, are wrapped by an `untrusted.*` type.

#### Nested containers

Lazily nested containers are fully supported, too:

    someValues = [
        ["apple","banana","orange", "pineapple"],
        ["cat", "dog", "monkey", "elephant"],
        ["green", "yellow", "blue", "rainbow"],
    ]

    seq = untrusted.sequenceOf(untrusted.sequence)

    for catagory in seq(someValues):
        for item in catagory:
            print(item.escape(someEscapeMethod, ...))



## Notes of Caution

### Different contexts

Remember, just because you have used one method to escape an `untrusted.string`
into a `str`, it may not be safe in other contexts. For example, what's safe
for HTML might still be dangerous SQL. It's best to delay the escaping until
the final point of use - keep a value as `untrusted.*` for as long as possible.

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


### Using untrusted collection types

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

