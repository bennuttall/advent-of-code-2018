from itertools import product

test_data = {
    'aA': 0,
    'abBA': 0,
    'abAB': 4,
    'aabAAB': 6,
    'dabAcCaCBAcCcaDA': 10,
}

alphabet = 'abcdefghijklmnopqrstuvwxyz'

replacements = ([f'{char}{char.upper()}' for char in alphabet] +
                [f'{char.upper()}{char}' for char in alphabet])

def replace(s):
    while any(rep in s for rep in replacements):
        for rep in replacements:
            s = s.replace(rep, '')
    return len(s)

for s, n in test_data.items():
    assert replace(s) == n, (s, n)

with open('input') as inp:
    data = inp.read().strip()

print(replace(data))
