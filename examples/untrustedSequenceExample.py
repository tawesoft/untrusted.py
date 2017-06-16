import html # for html.escape
import untrusted


# list of strings from an untrusted source
fruits = ["apple","banana","orange", "pineapple"]
animals = ["cat", "dog", "monkey", "elephant", "<big>mouse</big>"]
colors = ["green", "yellow", "blue", "rainbow", "<span color=\"green\">red</span>"]

untrustedAnimalList = untrusted.sequence(animals)
print(repr(untrustedAnimalList))

assert "cat" in untrustedAnimalList
assert not "green" in untrustedAnimalList

print("List of animals (HTML safe):")
for animal in untrustedAnimalList:
    try:
        print(animal) # won't work!
    except TypeError:
        print("Can't print(animal) without escaping it first!")

    print(animal.escape(html.escape))


firstAnimal, *restOfAnimals = untrustedAnimalList
print(("The first animal is: "+firstAnimal).escape(html.escape))

# Like normal Python 3 list slices, a slice of an untrsuted.list is a copy, not a view
print("The rest of animals are: "+repr(restOfAnimals))



# Nesting - here's a list of list of strings
someValues = [fruits, animals, colors]

untrustedValues = untrusted.sequence(someValues, valueType=untrusted.sequence)

for things in untrustedValues:
    print("A list of related things: ")
    for thing in things:
        print(repr(thing))
    print("things is " + repr(things))
    s = 'My list is: ' + untrusted.string(', ').join(things).escape(html.escape)
    print(s)
    s = "My list reversed is: " + untrusted.string(', ').join(reversed(things)).escape(html.escape)
    print(s)



