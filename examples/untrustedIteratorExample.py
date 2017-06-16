
import html # html.escape
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
    ["green", "red", "rainbow", "<span color=\"green\">red</span>"]
]

myIteratorType = untrusted.iteratorOf(untrusted.iterator)
it = myIteratorType(someValues)

for things in it:
    print("A list of related things: ")
    for thing in things:
        print(repr(thing))
    print("things is " + repr(things))
    s = 'My list is: ' + untrusted.string(', ').join(things).escape(html.escape)
    print(s)

