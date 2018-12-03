from itertools import product

with open('input') as inp:
    data = [line.strip() for line in inp.readlines()]

def count_overlap(data):
    fabric = set()
    overlap = set()
    for item in data:
        before_size = len(fabric)
        id, x, y, w, h = get_item_data(item)
        claim = product(range(x, x+w), range(y, y+h))
        for pos in claim:
            if pos in fabric:
                overlap.add(pos)
            fabric.add(pos)
    return len(overlap)

def get_item_data(item):
    parts = item.split(' ')
    id = int(parts[0].replace('#', ''))
    x, y = [int(i) for i in parts[2].replace(':', '').split(',')]
    w, h = [int(i) for i in parts[3].split('x')]
    return (id, x, y, w, h)

def find_unique_claim(data):
    for item in data:
        fabric = set()
        for item2 in data:
            if item == item2:
                continue
            id, x, y, w, h = get_item_data(item2)
            claim = set(product(range(x, x+w), range(y, y+h)))
            fabric.update(claim)
        id, x, y, w, h = get_item_data(item)
        claim = set(product(range(x, x+w), range(y, y+h)))
        if all(pos not in fabric for pos in claim):
            return id

test_data = """#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2""".split('\n')

assert count_overlap(test_data) == 4
assert find_unique_claim(test_data) == 3

if __name__ == '__main__':
    print(count_overlap(data))
    print(find_unique_claim(data))
