import html # for html.escape
import untrusted


# list of strings from an untrusted source
fruits = ["apple","banana","orange", "pineapple"]
animals = ["cat", "dog", "monkey", "elephant", "<big>mouse</big>"]
colors = ["green", "yellow", "blue", "rainbow", "<span color=\"green\">red</span>"]

untrustedAnimalList = untrusted.sequence(animals)
print(repr(untrustedAnimalList))

print("List of animals (HTML safe):")
for animal in untrustedAnimalList:
    try:
        print(animal) # won't work!
    except TypeError:
        print("Can't print(animal) without escaping it first!")

    print(animal.escape(html.escape))


firstAnimal = untrustedAnimalList[0]



# list of list of strings
someValues = [fruits, animals, colors]




