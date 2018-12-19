test_data = [
    'abcdef',
    'bababc',
    'abbcde',
    'abcccd',
    'aabcdd',
    'abcdee',
    'ababab',
]

test_data_2 = [
    'abcde',
    'fghij',
    'klmno',
    'pqrst',
    'fguij',
    'axcye',
    'wvxyz',
]

def check(id, n):
    return any(id.count(c) == n for c in set(id))

def checksum(data):
    two = three = 0
    for id in data:
        if check(id, 2):
            two += 1
        if check(id, 3):
            three += 1
    return two * three

def correct_letters(data):
    ida, idb = find_close_ids(data)
    for i, (ca, cb) in enumerate(zip(ida, idb)):
        if ca != cb:
            return ida[:i] + ida[i+1:]

def find_close_ids(data):
    for ida in data:
        for idb in data:
            if compare(ida, idb) == 1:
                return (ida, idb)

def compare(ida, idb):
    s = 0
    for ca, cb in zip(ida, idb):
        if ca != cb:
            s += 1
    return s

assert checksum(test_data) == 12
assert correct_letters(test_data_2) == 'fgij'

with open('input') as inp:
    data = [s.strip() for s in inp.readlines()]

print(checksum(data))
print(correct_letters(data))
