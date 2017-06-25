# This file contains fairly exhaustive tests of almost all the methods
# supported by the Python `str` type, and tests that `untrusted.string` type:
# * correctly supports the same methods
# * accepts `str` and/or `untrusted.string` arguments interchangeably
# * never returns `str` or any iterable of `str`, only an
#   appropriate `untrusted.*` type.
# Also tests that subclassed instances of untrusted.string work


import untrusted
from sys import stderr
import html


class customstring(untrusted.string):
    pass


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


# Test the test
assert same("cat", "cat")
assert not same("cat", "dog")

assert same(untrusted.string("cat"), untrusted.string("cat"))
assert not same(untrusted.string("cat"), untrusted.string("dog"))

assert not same(untrusted.string("cat"), "cat")
assert not same("cat", untrusted.string("cat"))

assert not same("cat", None)
assert not same(untrusted.string("cat"), None)

assert not same(untrusted.string("cat"), customstring("cat"))

assert same(None, None)


# Test an untrusted.string is never None!
try:
    _ = untrusted.string(None)
    raise AssertionError
except TypeError:
    pass


# Test an untrusted.string doesn't print!
try:
    print(untrusted.string("Hello"))
    raise AssertionError
except TypeError:
    pass # expected!


# Test the subclassed string doesn't print!
try:
    print(customstring("Hello"))
    raise AssertionError
except TypeError:
    pass # expected!



# container iteration
for i in "cat":
    assert i in ("c", "a", "t")

for i in untrusted.string("cat"):
    assert i in ("c", "a", "t")
    assert same(i, untrusted.string("c")) or same(i, untrusted.string("a")) or same(i, untrusted.string("t"))


# "Strings implement all of the common sequence operations"
# https://docs.python.org/3.4/library/stdtypes.html#typesseq-common


# membership: x in s
assert "a" in "cat"
assert "a" in untrusted.string("cat")
assert untrusted.string("a") in untrusted.string("cat")

assert not ("b" in "cat")
assert not ("b" in untrusted.string("cat"))
assert not (untrusted.string("b") in untrusted.string("cat"))

assert "cat" in "dogcatmouse"
assert "cat" in untrusted.string("dogcatmouse")
assert untrusted.string("cat") in untrusted.string("dogcatmouse")

assert customstring("a") in untrusted.string("cat")
assert untrusted.string("a") in customstring("a")


# membership: x not in s
assert "b" not in "cat"
assert "b" not in untrusted.string("cat")
assert untrusted.string("b") not in untrusted.string("cat")

assert not ("a" not in "cat")
assert not ("a" not in untrusted.string("cat"))
assert not (untrusted.string("a") not in untrusted.string("cat"))

assert customstring("b") not in untrusted.string("cat")


# concatenation: s + t
assert same("cat"+"dog", "catdog")
assert same(untrusted.string("cat") + "dog", untrusted.string("catdog"))
assert same("cat" + untrusted.string("dog"), untrusted.string("catdog"))
assert same(untrusted.string("cat") + untrusted.string("dog"), untrusted.string("catdog"))

# concatination with subclasses - becomes left-most class
assert same(untrusted.string("a") + customstring("b"), untrusted.string("ab"))
assert same(customstring("a") + untrusted.string("b"), customstring("ab"))


# s * n or n * s - "equivalent to adding s to itself n times"
assert same(3*"cat", "catcatcat")
assert same(3*untrusted.string("cat"), untrusted.string("catcatcat"))
assert same(3*customstring("cat"), customstring("catcatcat"))
assert same("cat"*3, "catcatcat")
assert same(untrusted.string("cat")*3, untrusted.string("catcatcat"))
assert same(customstring("cat")*3, customstring("catcatcat"))

assert same(0*"cat", "")
assert same(0*untrusted.string("cat"), untrusted.string(""))
assert same("cat"*0, "")
assert same(untrusted.string("cat")*0, untrusted.string(""))

# s[i] - item at index i
assert same("cat"[1], "a")
assert same(untrusted.string("cat")[1], untrusted.string("a"))

assert same("cat"[-1], "t")
assert same(untrusted.string("cat")[-1], untrusted.string("t"))

try:
    _ = "cat"[4]
    raise AssertionError
except IndexError:
    pass # expected!

try:
    _ = untrusted.string("cat")[4]
    raise AssertionError
except IndexError:
    pass # expected!


# s[i:j:k] - slice i to j with step k
assert same("dogcatmouse"[3:6], "cat")
assert same(untrusted.string("dogcatmouse")[3:6], untrusted.string("cat"))
assert same(customstring("dogcatmouse")[3:6], customstring("cat"))

assert same("dogcatmouse"[3:6:2], "ct")
assert same(untrusted.string("dogcatmouse")[3:6:2], untrusted.string("ct"))
assert same(customstring("dogcatmouse")[3:6:2], customstring("ct"))


# len(s)
assert len("cat") == 3
assert len(untrusted.string("cat")) == 3


#min(s)	smallest item of s	 
assert same(min("cat"), "a")
assert same(min(untrusted.string("cat")), untrusted.string("a"))


#max(s)	largest item of s	 
assert same(max("cat"), "t")
assert same(max(untrusted.string("cat")), untrusted.string("t"))


# s.index(x[, i[, j]])
# "index of the first occurrence of x in s
# (at or after index i and before index j)"
assert "cat".index("a") == 1
assert untrusted.string("cat").index("a") == 1

assert "dogcatmouse".index("cat") == 3
assert untrusted.string("dogcatmouse").index("cat") == 3
assert untrusted.string("dogcatmouse").index(untrusted.string("cat")) == 3


# s.count(x) - occurrences of x in s
assert "cat".count("a") == 1
assert untrusted.string("cat").count("a") == 1
assert untrusted.string("cat").count(untrusted.string("a")) == 1

assert "cataclasm".count("a") == 3
assert untrusted.string("cataclasm").count("a") == 3
assert untrusted.string("cataclasm").count(untrusted.string("a")) == 3

assert "cat attack".count("at") == 2
assert untrusted.string("cat attack").count("at") == 2
assert untrusted.string("cat attack").count(untrusted.string("at")) == 2


# x.join(y)
assert same(''.join([]), "")
assert same(untrusted.string('').join([]), untrusted.string(""))

assert same(''.join("cat"), "cat")
assert same(untrusted.string('').join("cat"), untrusted.string("cat"))
assert same(untrusted.string('').join(untrusted.string("cat")), untrusted.string("cat"))

assert same(','.join(["cat", "dog", "mouse"]), "cat,dog,mouse")
assert same(untrusted.string(',').join(["cat", "dog", "mouse"]), untrusted.string("cat,dog,mouse"))
assert same(untrusted.string(',').join([untrusted.string("cat"), untrusted.string("dog"), untrusted.string("mouse")]), untrusted.string("cat,dog,mouse"))

# sorry, str('').join(untrusted.string(...)) won't work
# but let's make sure we get an exception
# to be certain that an untrusted.string doesn't ever leak into a normal str
try:
    _ = ''.join(untrusted.string("hello"))
    raise AssertionError
except TypeError:
    pass # expected

try:
    _ = ''.join(customstring("hello"))
    raise AssertionError
except TypeError:
    pass # expected


# x.reversed()
assert same(''.join(reversed("cat")), "tac")
assert same(untrusted.string('').join(reversed(untrusted.string("cat"))), untrusted.string("tac"))


# iteration
for i in "cat":
    assert same(i, "c") or same(i, "a") or same(i, "t")

for i in untrusted.string("cat"):
    assert same(i, untrusted.string("c")) or same(i, untrusted.string("a")) or same(i, untrusted.string("t"))



# string methods
# https://docs.python.org/3.4/library/stdtypes.html#string-methods

# str.capitalize()
assert same("cAt".capitalize(), "Cat")
assert same(untrusted.string("cAt").capitalize(), untrusted.string("Cat"))


# str.casefold()
assert same("Catß".casefold(), "catss")
assert same(untrusted.string("Catß").casefold(), untrusted.string("catss"))

# str.center(width[, fillchar])
assert same("cat".center(7), "  cat  ")
assert same(untrusted.string("cat").center(7), untrusted.string("  cat  "))
assert same("cat".center(7, "-"), "--cat--")
assert same(untrusted.string("cat").center(7, "-"), untrusted.string("--cat--"))
assert same(untrusted.string("cat").center(7, untrusted.string("-")), untrusted.string("--cat--"))

# str.count(sub[, start[, end]])
assert "dogcatmousecat".count("cat", 0, 3) == 0
assert "dogcatmousecat".count("cat", 3, 6) == 1
assert "dogcatmousecat".count("cat", 3) == 2

assert untrusted.string("dogcatmousecat").count("cat", 0, 3) == 0
assert untrusted.string("dogcatmousecat").count("cat", 3, 6) == 1
assert untrusted.string("dogcatmousecat").count("cat", 3) == 2

assert untrusted.string("dogcatmousecat").count(untrusted.string("cat"), 0, 3) == 0
assert untrusted.string("dogcatmousecat").count(untrusted.string("cat"), 3, 6) == 1
assert untrusted.string("dogcatmousecat").count(untrusted.string("cat"), 3) == 2


# str.encode
# disabled on purpose for untrusted.string!!!

assert same("cat".encode("ascii"), b"cat")

try:
    _ = untrusted.string("cat").encode("ascii")
    raise AssertionError
except TypeError:
    pass # expected!


# str.endswith(suffix[, start[, end]])
assert "catdogmouse".endswith("mouse")
assert untrusted.string("catdogmouse").endswith("mouse")
assert untrusted.string("catdogmouse").endswith(untrusted.string("mouse"))

assert not "catdogmouse".endswith("cat")
assert not untrusted.string("catdogmouse").endswith("cat")
assert not untrusted.string("catdogmouse").endswith(untrusted.string("cat"))

assert "catdogmouse".endswith("dog", 0, 6)
assert untrusted.string("catdogmouse").endswith("dog", 0, 6)
assert untrusted.string("catdogmouse").endswith(untrusted.string("dog"), 0, 6)

assert not "catdogmouse".endswith("dog", 4)
assert not untrusted.string("catdogmouse").endswith("dog", 4)
assert not untrusted.string("catdogmouse").endswith(untrusted.string("dog"), 4)


# str.expandtabs(tabsize=8)
assert same("\tHello\tworld!".expandtabs(), "        Hello   world!")
assert same(untrusted.string("\tHello\tworld!").expandtabs(), untrusted.string("        Hello   world!"))


# str.find(sub[, start[, end]])
assert "dogcatmouse".find("cat") == 3
assert untrusted.string("dogcatmouse").find("cat") == 3
assert untrusted.string("dogcatmouse").find(untrusted.string("cat")) == 3

assert "dogcatmouse".find("cat", 4) == -1
assert untrusted.string("dogcatmouse").find("cat", 4) == -1
assert untrusted.string("dogcatmouse").find(untrusted.string("cat"), 4) == -1


# str.format(*args, **kwargs)

# with numeric argument:

assert same(
    "Hello {0}, UserID: {1}".format("Sarah", 123),
    "Hello Sarah, UserID: 123"
)

assert same(
    untrusted.string("Hello {0}, UserID: {1}").format("Sarah", 123),
    untrusted.string("Hello Sarah, UserID: 123")
)

assert same(
    untrusted.string("Hello {0}, UserID: {1}").format(untrusted.string("Sarah"), 123),
    untrusted.string("Hello Sarah, UserID: 123")
)


# ensure untrusted.string never leaks into a str...
try:
    _ =  "Hello {0}, UserID: {1}".format(untrusted.string("Sarah"), 123),
    raise AssertionError
except TypeError:
    pass # expected!



# with named arguments:

assert same(
    "Hello {name}, UserID: {uid}".format(name="Sarah", uid=123),
    "Hello Sarah, UserID: 123"
)

assert same(
    untrusted.string("Hello {name}, UserID: {uid}").format(name="Sarah", uid=123),
    untrusted.string("Hello Sarah, UserID: 123")
)

assert same(
    untrusted.string("Hello {name}, UserID: {uid}").format(name=untrusted.string("Sarah"), uid=123),
    untrusted.string("Hello Sarah, UserID: 123")
)



# str.format_map(mapping)
assert same(
    "Hello {name}, UserID: {uid}".format_map({"name": "Sarah", "uid": 123}),
    "Hello Sarah, UserID: 123"
)

assert same(
    untrusted.string("Hello {name}, UserID: {uid}").format_map({"name": "Sarah", "uid": 123}),
    untrusted.string("Hello Sarah, UserID: 123")
)

assert same(
    untrusted.string("Hello {name}, UserID: {uid}").format_map({"name": untrusted.string("Sarah"), "uid": "123"}),
    untrusted.string("Hello Sarah, UserID: 123")
)


# advanced! format_map with an untrusted.mapping!!
myUntrustedDict = untrusted.mapping({'name': 'Sarah', "uid": "123"})

assert same(
    untrusted.string("Hello {name}, UserID: {uid}").format_map(myUntrustedDict),
    untrusted.string("Hello Sarah, UserID: 123")
)


# An untrusted mapping with untrusted keys is not allowed to format a string
# This is by design!
myUntrustedDict = untrusted.mappingOf(untrusted.string, untrusted.string)({'name': 'Sarah', "uid": "123"})

try:
    assert same(
        untrusted.string("Hello {name}, UserID: {uid}").format_map(myUntrustedDict),
        untrusted.string("Hello Sarah, UserID: 123")
    )
    raise AssrtionError
except TypeError:
    pass # expected


# ensure untrusted.mapping never leaks into a str...
try:
    _ =  "Hello {name}, UserID: {uid}".format_map(myUntrustedDict),
    raise AssertionError
except TypeError:
    pass # expected!


# str.index(sub[, start[, end]])
# "Like find(), but raise ValueError when the substring is not found."

assert "dogcatmouse".index("cat") == 3
assert untrusted.string("dogcatmouse").index("cat") == 3
assert untrusted.string("dogcatmouse").index(untrusted.string("cat")) == 3

try:
    _ = "dogcatmouse".index("tiger")
    raise AssertionError
except ValueError:
    pass # expected

try:
    _ = untrusted.string("dogcatmouse").index("tiger")
    raise AssertionError
except ValueError:
    pass # expected

try:
    _ = untrusted.string("dogcatmouse").index(untrusted.string("tiger"))
    raise AssertionError
except ValueError:
    pass # expected

try:
    _ = "dogcatmouse".index("cat", 4)
    raise AssertionError
except ValueError:
    pass # expected

try:
    _ = untrusted.string("dogcatmouse").index("cat", 4)
    raise AssertionError
except ValueError:
    pass # expected

try:
    _ = untrusted.string("dogcatmouse").index(untrusted.string("cat"), 4)
    raise AssertionError
except ValueError:
    pass # expected


# str.isalnum()
assert "cat".isalnum()
assert untrusted.string("cat").isalnum()
assert not "£123".isalnum()
assert not untrusted.string("£123").isalnum()

# str.isalpha()
assert "cat".isalpha()
assert untrusted.string("cat").isalpha()
assert not "123".isalpha()
assert not untrusted.string("123").isalpha()

# str.isdecimal()
assert "123".isdecimal()
assert untrusted.string("123").isdecimal()
assert not "cat".isdecimal()
assert not untrusted.string("cat").isdecimal()

# str.isdigit()
assert "2²".isdigit()
assert untrusted.string("2²").isdigit()

# str.isidentifier()
assert "hello".isidentifier()
assert untrusted.string("hello").isidentifier()
assert not "123".isidentifier()
assert not untrusted.string("123").isidentifier()

# str.islower()
assert "hello".islower()
assert untrusted.string("hello").islower()
assert not "Hello".islower()
assert not untrusted.string("Hello").islower()

# str.isnumeric()
assert "123".isnumeric()
assert untrusted.string("123").isnumeric()
assert not "hello".isnumeric()
assert not untrusted.string("hello").isnumeric()

# str.isprintable()
assert "123".isprintable()
assert untrusted.string("123").isprintable()
assert not "\01".isprintable()
assert not untrusted.string("\01").isprintable()

# str.isspace()
assert "    \t\r\n".isspace()
assert untrusted.string("    \t\r\n").isspace()
assert not "cat".isspace()
assert not untrusted.string("cat").isspace()

# str.istitle()
assert "Hello World".istitle()
assert untrusted.string("Hello World").istitle()
assert not "hello world".istitle()
assert not untrusted.string("hello world").istitle()

# str.isupper()
assert "CAT".isupper()
assert untrusted.string("CAT").isupper()
assert not "cat".isupper()
assert not untrusted.string("cat").isupper()

# str.join(iterable) - done

# str.ljust(width[, fillchar])
assert same("CAT".ljust(8, "-"), "CAT-----")
assert same(untrusted.string("CAT").ljust(8, "-"), untrusted.string("CAT-----"))

# str.lower()
assert same("Cat".lower(), "cat")
assert same(untrusted.string("Cat").lower(), untrusted.string("cat"))

# str.lstrip([chars])
assert same(" cat".lstrip(), "cat")
assert same(untrusted.string(" cat".lstrip()), untrusted.string("cat"))
assert same(" cat".lstrip(" ca"), "t")
assert same(untrusted.string(" cat").lstrip(" ca"), untrusted.string("t"))
assert same(untrusted.string(" cat").lstrip(untrusted.string(" ca")), untrusted.string("t"))
assert same(untrusted.string(" cat").lstrip(customstring(" ca")), untrusted.string("t"))


# str.partition(sep)

# no result
parts = "cat,dog,mouse".partition("X")
a, b, c = parts
assert same(a, "cat,dog,mouse")
assert same(b, "")
assert same(c, "")

parts = untrusted.string("cat,dog,mouse").partition("X")
a, b, c = parts
assert same(a, untrusted.string("cat,dog,mouse"))
assert same(b, untrusted.string(""))
assert same(c, untrusted.string(""))

parts = untrusted.string("cat,dog,mouse").partition(untrusted.string("X"))
a, b, c = parts
assert same(a, untrusted.string("cat,dog,mouse"))
assert same(b, untrusted.string(""))
assert same(c, untrusted.string(""))

parts = customstring("cat,dog,mouse").partition(untrusted.string("X"))
a, b, c = parts
assert same(a, customstring("cat,dog,mouse"))
assert same(b, customstring(""))
assert same(c, customstring(""))

parts = untrusted.string("cat,dog,mouse").partition(customstring("X"))
a, b, c = parts
assert same(a, untrusted.string("cat,dog,mouse"))
assert same(b, untrusted.string(""))
assert same(c, untrusted.string(""))

# result
parts = "cat,dog,mouse".partition(",")
a, b, c = parts
assert same(a, "cat")
assert same(b, ",")
assert same(c, "dog,mouse")

parts = untrusted.string("cat,dog,mouse").partition(",")
a, b, c = parts
assert same(a, untrusted.string("cat"))
assert same(b, untrusted.string(","))
assert same(c, untrusted.string("dog,mouse"))

parts = untrusted.string("cat,dog,mouse").partition(untrusted.string(","))
a, b, c = parts
assert same(a, untrusted.string("cat"))
assert same(b, untrusted.string(","))
assert same(c, untrusted.string("dog,mouse"))

parts = customstring("cat,dog,mouse").partition(untrusted.string(","))
a, b, c = parts
assert same(a, customstring("cat"))
assert same(b, customstring(","))
assert same(c, customstring("dog,mouse"))

parts = untrusted.string("cat,dog,mouse").partition(customstring(","))
a, b, c = parts
assert same(a, untrusted.string("cat"))
assert same(b, untrusted.string(","))
assert same(c, untrusted.string("dog,mouse"))


# str.replace(old, new[, count])
assert same("cat,dog,hat".replace("at", "ave"), "cave,dog,have")
assert same(untrusted.string("cat,dog,hat").replace("at", "ave"), untrusted.string("cave,dog,have"))
assert same(untrusted.string("cat,dog,hat").replace(untrusted.string("at"), untrusted.string("ave")), untrusted.string("cave,dog,have"))

# str.rfind(sub[, start[, end]])
assert "dogcathat".rfind("at") == 7
assert untrusted.string("dogcathat").rfind("at") == 7
assert untrusted.string("dogcathat").rfind(untrusted.string("at")) == 7

assert "dogcathat".rfind("mouse") == -1
assert untrusted.string("mouse").rfind("at") == -1
assert untrusted.string("mouse").rfind(untrusted.string("at")) == -1


# str.rindex(sub[, start[, end]])
# Like rfind() but raises ValueError when the substring sub is not found.
try:
    _ = "dogcatmouse".rindex("tiger")
    raise AssertionError
except ValueError:
    pass # expected

try:
    _ = untrusted.string("dogcatmouse").rindex("tiger")
    raise AssertionError
except ValueError:
    pass # expected

try:
    _ = untrusted.string("dogcatmouse").rindex(untrusted.string("tiger"))
    raise AssertionError
except ValueError:
    pass # expected

try:
    _ = untrusted.string("dogcatmouse").rindex(customstring("tiger"))
    raise AssertionError
except ValueError:
    pass # expected


# str.rpartition(sep)
# no result
parts = "cat,dog,mouse".rpartition("X")
a, b, c = parts
assert same(a, "")
assert same(b, "")
assert same(c, "cat,dog,mouse")

parts = untrusted.string("cat,dog,mouse").rpartition("X")
a, b, c = parts
assert same(a, untrusted.string(""))
assert same(b, untrusted.string(""))
assert same(c, untrusted.string("cat,dog,mouse"))

parts = untrusted.string("cat,dog,mouse").rpartition(untrusted.string("X"))
a, b, c = parts
assert same(a, untrusted.string(""))
assert same(b, untrusted.string(""))
assert same(c, untrusted.string("cat,dog,mouse"))

parts = customstring("cat,dog,mouse").rpartition(untrusted.string("X"))
a, b, c = parts
assert same(a, customstring(""))
assert same(b, customstring(""))
assert same(c, customstring("cat,dog,mouse"))

parts = untrusted.string("cat,dog,mouse").rpartition(customstring("X"))
a, b, c = parts
assert same(a, untrusted.string(""))
assert same(b, untrusted.string(""))
assert same(c, untrusted.string("cat,dog,mouse"))

# result
parts = "cat,dog,mouse".rpartition(",")
a, b, c = parts
assert same(a, "cat,dog")
assert same(b, ",")
assert same(c, "mouse")

parts = untrusted.string("cat,dog,mouse").rpartition(",")
a, b, c = parts
assert same(a, untrusted.string("cat,dog"))
assert same(b, untrusted.string(","))
assert same(c, untrusted.string("mouse"))

parts = untrusted.string("cat,dog,mouse").rpartition(untrusted.string(","))
a, b, c = parts
assert same(a, untrusted.string("cat,dog"))
assert same(b, untrusted.string(","))
assert same(c, untrusted.string("mouse"))

parts = customstring("cat,dog,mouse").rpartition(untrusted.string(","))
a, b, c = parts
assert same(a, customstring("cat,dog"))
assert same(b, customstring(","))
assert same(c, customstring("mouse"))

parts = untrusted.string("cat,dog,mouse").rpartition(customstring(","))
a, b, c = parts
assert same(a, untrusted.string("cat,dog"))
assert same(b, untrusted.string(","))
assert same(c, untrusted.string("mouse"))


# str.rsplit(sep=None, maxsplit=-1)

parts = "a,b,c,d".rsplit(",", maxsplit=2)
rest,c,d = parts
assert same(rest, "a,b")
assert same(c, "c")
assert same(d, "d")


parts = untrusted.string("a,b,c,d").rsplit(",", maxsplit=2)
rest,c,d = parts
assert same(rest, untrusted.string("a,b"))
assert same(c, untrusted.string("c"))
assert same(d, untrusted.string("d"))


parts = untrusted.string("a,b,c,d").rsplit(untrusted.string(","), maxsplit=2)
rest,c,d = parts
assert same(rest, untrusted.string("a,b"))
assert same(c, untrusted.string("c"))
assert same(d, untrusted.string("d"))


# str.rstrip([chars])
assert same("cat ".rstrip(), "cat")
assert same(untrusted.string("cat ".rstrip()), untrusted.string("cat"))
assert same("cat ".rstrip(" ta"), "c")
assert same(untrusted.string("cat ").rstrip(" ta"), untrusted.string("c"))
assert same(untrusted.string("cat ").rstrip(untrusted.string(" ta")), untrusted.string("c"))
assert same(untrusted.string("cat ").rstrip(customstring(" ta")), untrusted.string("c"))


# str.split(sep=None, maxsplit=-1)

parts = "a,b,c,d".split(",", maxsplit=2)
a,b,rest = parts
assert same(a, "a")
assert same(b, "b")
assert same(rest, "c,d")


parts = untrusted.string("a,b,c,d").split(",", maxsplit=2)
a,b,rest = parts
assert same(a, untrusted.string("a"))
assert same(b, untrusted.string("b"))
assert same(rest, untrusted.string("c,d"))


parts = untrusted.string("a,b,c,d").split(untrusted.string(","), maxsplit=2)
a,b,rest = parts
assert same(a, untrusted.string("a"))
assert same(b, untrusted.string("b"))
assert same(rest, untrusted.string("c,d"))

parts = customstring("a,b,c,d").split(",", maxsplit=2)
a,b,rest = parts
assert same(a, customstring("a"))
assert same(b, customstring("b"))
assert same(rest, customstring("c,d"))

parts = customstring("a,b,c,d").split(untrusted.string(","), maxsplit=2)
a,b,rest = parts
assert same(a, customstring("a"))
assert same(b, customstring("b"))
assert same(rest, customstring("c,d"))


# str.strip([chars])
assert same(" cat ".strip(), "cat")
assert same(untrusted.string(" cat ".strip()), untrusted.string("cat"))
assert same(" cat ".strip(" ct"), "a")
assert same(untrusted.string(" cat ").strip(" ct"), untrusted.string("a"))
assert same(untrusted.string(" cat ").strip(untrusted.string(" ct")), untrusted.string("a"))
assert same(untrusted.string(" cat ").strip(customstring(" ct")), untrusted.string("a"))

# str.swapcase()
assert same("Cat".swapcase(), "cAT")
assert same(untrusted.string("Cat").swapcase(), untrusted.string("cAT"))
assert same(customstring("Cat").swapcase(), customstring("cAT"))

# str.title()
assert same("hello world".title(), "Hello World")
assert same(untrusted.string("hello world").title(), untrusted.string("Hello World"))

# str.upper()
assert same("hello world".upper(), "HELLO WORLD")
assert same(untrusted.string("hello world").upper(), untrusted.string("HELLO WORLD"))

# str.zfill(width)
assert same("42".zfill(5), "00042")
assert same(untrusted.string("42").zfill(5), untrusted.string("00042"))
assert same("-42".zfill(5), "-0042")
assert same(untrusted.string("-42").zfill(5), untrusted.string("-0042"))


# TODO str.translate - not impleemnted
# TODO str.maketrans - not implemented


# hashable: a set of strings
parts = set(["cat", "dog", "tiger"])
assert "cat" in parts

parts = set([untrusted.string("cat"), untrusted.string("dog"), untrusted.string("tiger")])
assert "cat" in parts
assert untrusted.string("cat") in parts
assert customstring("cat") in parts


# %-style format also with a number
assert same("Hello %s aged %d" % ("Grace", 101), "Hello Grace aged 101")
assert same(untrusted.string("Hello %s aged %d") % ("Grace", 101), untrusted.string("Hello Grace aged 101"))
assert same(untrusted.string("Hello %s aged %d") % (untrusted.string("Grace"), 101), untrusted.string("Hello Grace aged 101"))

# %-style dict format (rare) also with with number
assert same("Hello %(name)s aged %(age)d" % {"name": "Grace", "age": 101}, "Hello Grace aged 101")
assert same(untrusted.string("Hello %(name)s aged %(age)d") % {"name": "Grace", "age": 101}, untrusted.string("Hello Grace aged 101"))
assert same(untrusted.string("Hello %(name)s aged %(age)d") % {"name": untrusted.string("Grace"), "age": 101}, untrusted.string("Hello Grace aged 101"))


# An untrusted mapping with untrusted keys is not allowed to format a string
# This is by design!
try:
    _ = same(untrusted.string("Hello %(name)s aged %(age)d") % {untrusted.string("name"): untrusted.string("Grace"), "age": 101}, untrusted.string("Hello Grace aged 101"))
    raise AssrtionError
except TypeError:
    pass # expected



# escape examples
before = "<b>\"Hello\"</b>"
after_qt = "&lt;b&gt;&quot;Hello&quot;&lt;/b&gt;"
after_unqt =  "&lt;b&gt;\"Hello\"&lt;/b&gt;"

assert same(html.escape(before), after_qt)
assert same(untrusted.string(before).escape(html.escape), after_qt)
assert same(customstring(before).escape(html.escape), after_qt)

assert same(untrusted.string(before) / html.escape, after_qt)
assert same(customstring(before) / html.escape, after_qt)

assert same(html.escape(before, quote=False), after_unqt)
assert same(untrusted.string(before).escape(html.escape, quote=False), after_unqt)
assert same(customstring(before).escape(html.escape, quote=False), after_unqt)

assert same(untrusted.string(before) / (html.escape, [], {'quote': False}), after_unqt)
assert same(customstring(before) / (html.escape, [], {'quote': False}), after_unqt)






