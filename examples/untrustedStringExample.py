import untrusted

# untrusted.string example
#-------------------------------------------------------------------------------

# The `untrusted.string` is a special string type. It behaves almost exactly
# like a normal string of type `str` - except, it cannot be implicitly used
# where a normal string is expected, e.g. in print or other functions. This
# improves security by preventing untrusted input being used by accident.

a = untrusted.string("Hello")
b = untrusted.string("World!")

try:
    print(a)
except TypeError:
    print("print(a) was disallowed!")

print("repr(a) is: %s" % repr(a))
print("repr(b) is: %s" % repr(b))


# comparason with normal str values is fine
assert untrusted.string("cat") == str("cat")


# You can add strings and untrusted.strings together, and the result is a
# new `untrusted.string` .

c = a + ', ' + b

print("repr(c) is: %s" % repr(c)) # <untrusted.string: 'Hello, World!'>


d = 'Goodbye ' + b

print("repr(d) is: %s" % repr(d)) # <untrusted.string: 'Goodbye World!'>


# You can use all of the `str` methods you expect. These are whitelisted
# so that we can be sure we didn't accidently miss any and create a potential
# vulnerability.

print("c.startswith('Hello'): %s" % c.startswith('Hello'))
print("repr(c.upper()): %s" % repr(c.upper()))


# This works with `untrusted.string` values as actual arguments too, because
# that helps things stay neat in pratice

print("c.startswith(untrusted.string('Goodbye')): %s" % c.startswith(untrusted.string('Goodbye')))


# Some methods return more complicated types, like tuples of
# `untrusted.string` values.
print("repr(c.partition(',')): %s" % repr(c.partition(',')))


# Or an `untrusted.sequence` of `untrusted.string` values.
things = untrusted.string("apple, banana, orange, mango")

print("repr(things): %s" % repr(things))

things = untrusted.string("apple, banana, orange, mango")
print("repr(things.split(','): %s" % repr(things.split(',')))
for i in things.split(','):
    print("    " + repr(i))

print("repr(things.split(',', maxsplit=1)): %s" % repr(things.split(',', maxsplit=1)))
for i in things.split(',', maxsplit=1):
    print("    " + repr(i))


# You can access the raw value by using the (read-only)  `value` property

markup = untrusted.string("<b>HTML \"Example\"</b>")
print("repr(markup): %s" % repr(markup))
print("repr(markup.value): %s" % repr(markup.value))


# Here's an example of escaping HTML

import html

print("html.escape(markup.value): %s" % html.escape(markup.value))
print("html.escape(markup.value): %s" % html.escape(markup.value, quote=False))


# But instead of faffing around with the value property, there's a convenient
# "escape" method that takes a method as an argument. Any other arguments
# are passed on to the given method. It also asserts that you actually get a
# `str` result.

print("markup.escape(html.escape): %s" % markup.escape(html.escape))
print("markup.escape(html.escape, quote=False): %s" % markup.escape(html.escape, quote=False))


# Here's an example using %-style formatting

template = "Hello %s!"
print(repr(template))
print(repr(template % "world"))

try:
    print(repr(template % untrusted.string("everyone")))
except TypeError:
    print("formatting using untrusted string was disallowed as expected!")



# Here's an example using `untrusted.string.format` (like `str.format`):

template = untrusted.string("Hello {name} this is my template")
print(repr(template))
result = template.format(name="Grace")
print(repr(result))
result = template.format(name=untrusted.string("Alan"))
print(repr(result))
result = template.format_map({'name': "Richie"})
print(repr(result))
result = template.format_map({'name': untrusted.string("Ada")})
print(repr(result))









