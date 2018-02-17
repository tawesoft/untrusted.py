import html # for html.escape
import untrusted


# a str -> untrusted.string mapping
user = untrusted.mapping({
    'username': 'example-username<b>hack attempt</b>',
    'password': 'example-password',
})

try:
    print(user.get("username")) # raises TypeError - untrusted.string used as a `str`!
except TypeError:
    print("Caught the error we expected!")

print(user.get("username", "default-username") / html.escape)



# a untrusted.string -> untrusted.string mapping

untrustedType = untrusted.mappingOf(untrusted.string, untrusted.string)

args = untrustedType({'animal': 'cat', '<b>hack</b>': 'attempt'})

for k,v in args.items():
    print("%s: %s" % (k / html.escape, v / html.escape))



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
mappingType = untrusted.iteratorOf(untrusted.mapping)

# aka (setting defaults explicitly)
mappingType = untrusted.iteratorOf(untrusted.mappingOf(str, untrusted.string))


for person in mappingType(people):
    for key, value in person.items():
        print("    %s: %s" % (key, value / html.escape))
    


