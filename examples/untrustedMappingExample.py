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
print("repr(mappingType(people)): %s" % repr(mappingType(people)))

for person in mappingType(people):
    print("repr(person): %s" % repr(person))
    for key, value in person.items():
        try:
            print("    %s = %s" % (key, value))
        except TypeError:
            # not allowed!
            pass
        print("    %s: repr(value)=%s" % (key, repr(value)))
    


