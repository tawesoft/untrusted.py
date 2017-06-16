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

This is a view over any iterable or generator yielding untrusted values.

#### `untrusted.sequence`

This is a view over any `list`-like object containing untrusted values.

#### `untrusted.mapping`

This a view over any `dict`-like object containing untrusted values and,
optionally, even untrusted keys.

#### Nested containers

Lazily nested containers are fully supported, too:

    someValues = [
        ["apple","banana","orange", "pineapple"],
        ["cat", "dog", "monkey", "elephant"],
        ["green", "yellow", "blue", "rainbow"],
    ]

    seq = untrusted.sequenceOf(untrusted.sequence)

    for i in seq(someValues):
        for j in i:
            print(j.escape(someEscapeMethod, ...))



## Notes of Caution

### Different contexts

Remember, just because you have used one method to escape an `untrusted.string`
into a `str`, it may not be safe in other contexts. For example, what's safe
for HTML might still be dangerous SQL. It's best to delay the escaping until
the final point of use - keep a value as `untrusted.*` for as long as possible.

This module isn't a magic solution. It's a tool to be used wisely.


### Using untrusted collection types

Untrusted collection types, like `untrusted.sequence`, are "views" over the
underling object. If the underlying object changes, so does the object you
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

