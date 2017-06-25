import html # for html.escape()
import untrusted

# example of a string that could be provided by an untrusted user
firstName = untrusted.string("Grace")
lastName = untrusted.string("<script>alert(\"hack attempt!\");</script>")

# works seamlessly with native python strings:
fullName = firstName + " " + lastName

# fullName keeps the untrusted.string type
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


# But what if you want to pass an argument to the escape function?

# Option One: make a new function

def myEscape1(x):
    return html.escape(x, quote=False)

myEscape2 = lambda x: html.escape(x, quote=False)

print("Without escaping quotes:")
print("<b>Escaped output:</b> " + fullName / myEscape1)
print("<b>Escaped output:</b> " + fullName / myEscape2)


# Option Two: escape method with extra arguments
print("<b>Escaped output:</b> " + fullName.escape(html.escape, quote=False))


# Option Three: escape shorthand with extra arguments
# as a tuple (function, args_list, kwargs_dict)
myEscape = (html.escape, [], {'quote': False})
print("<b>Escaped output:</b> " + fullName / myEscape)


