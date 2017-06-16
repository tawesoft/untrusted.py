
import untrusted

# untrusted.iterator example
#-------------------------------------------------------------------------------

# This is a simple iterator type for a single step over any iterable of
# untrusted values.

# The default type is an iterator of untrusted.strings

# it = untrusted.iterator(open("example.txt"), valueType=untrusted.string)

# Or, more simply,

it = untrusted.iterator(open("example.txt"))

print("repr(it): %s" % repr(it))

for i in it:
    print("repr(i): %s" % repr(i))


# You can come up with more complicated types, e.g. nested lists.
someValues = [
    ["cat", "dog", "zebra"],
    ["apple", "pear", "pineapple"],
    ["green", "red", "rainbow"]
]

it = untrusted.iterator(someValues, valueType=untrusted.iteratorOf(untrusted.string))

# Or, because iterators default to the untrusted.string type, more simply:

it = untrusted.iterator(someValues, valueType=untrusted.iterator)

for things in it:
    print("A list of related things: ")
    for thing in things:
        print(repr(thing))
    s = 'My list is: ' + untrusted.string(', ').join(things)
    print(repr(s))

