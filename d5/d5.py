from itertools import product
import operator

test_data = {
    'aA': (0, 0),
    'abBA': (0, 0),
    'abAB': (4, 0),
    'aabAAB': (6, 0),
    'dabAcCaCBAcCcaDA': (10, 4),
}

alphabet = 'abcdefghijklmnopqrstuvwxyz'

replacements = ([f'{char}{char.upper()}' for char in alphabet] +
                [f'{char.upper()}{char}' for char in alphabet])

def replace(s):
    while any(rep in s for rep in replacements):
        for rep in replacements:
            s = s.replace(rep, '')
    return len(s)

def find_best_replacement(s):
    return min(
        replace(s.replace(ch, '').replace(ch.upper(), '')) for ch in alphabet
    )

for s, n in test_data.items():
    assert replace(s) == n[0], (s, n[0])
    assert find_best_replacement(s) == n[1], (s, n[1])

with open('input') as inp:
    data = inp.read().strip()

print(replace(data))
print(find_best_replacement(data))
