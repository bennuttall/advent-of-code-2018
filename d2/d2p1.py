test_data = [
    'abcdef',
    'bababc',
    'abbcde',
    'abcccd',
    'aabcdd',
    'abcdee',
    'ababab',
]

with open('input') as inp:
    data = [s.strip() for s in inp.readlines()]

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

assert checksum(test_data) == 12

if __name__ == '__main__':
    print(checksum(data))
