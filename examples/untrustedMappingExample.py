import html # for html.escape
import untrusted

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
        print("    %s: %s" % (key, value.escape(html.escape)))
    


