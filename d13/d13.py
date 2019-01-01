import numpy as np
from itertools import cycle
from collections import namedtuple

Position = namedtuple('Position', ['x', 'y'])

class Cart:
    def __init__(self, x, y, c):
        self.pos = Position(x, y)
        self.c = c
        self.intersections = cycle('lsr')

    def __repr__(self):
        x, y = self.pos
        x2, y2 = self.next_pos
        c = self.c
        return f'Cart ({x}, {y}) {c} ({x2}, {y2})'

    def __str__(self):
        return self.c

    def __lt__(self, other):
        if self.pos.y < other.pos.y:
            return True
        elif self.pos.y == other.pos.y:
            return self.pos.x < other.pos.x
        return False

    def __next__(self):
        self.pos = self.next_pos
        return self.pos

    @property
    def next_pos(self):
        x, y = self.pos
        return {
            '^': Position(x, y-1),
            '>': Position(x+1, y),
            'v': Position(x, y+1),
            '<': Position(x-1, y),
        }[self.c]

    def corner(self, corner):
        c_before = self.c
        self.c = {
            ('^', '/'): '>',
            ('>', '/'): '^',
            ('v', '/'): '<',
            ('<', '/'): 'v',
            ('^', '\\'): '<',
            ('>', '\\'): 'v',
            ('v', '\\'): '>',
            ('<', '\\'): '^',
        }[(self.c, corner)]

    def intersection(self):
        c = next(self.intersections)
        if c == 's':
            return
        self.c = {
            ('l', '>'): '^',
            ('l', '^'): '<',
            ('l', '<'): 'v',
            ('l', 'v'): '>',
            ('r', '>'): 'v',
            ('r', '^'): '>',
            ('r', '<'): '^',
            ('r', 'v'): '<',
        }[(c, self.c)]

class MineCartMap:
    def __init__(self, map, crash_mode=False):
        self.carts = []
        self.read_map(map)
        self.crash = False
        self.crashed_carts = set()
        self.crash_mode = crash_mode

    def __str__(self):
        s = ''
        for y, col in enumerate(self.map):
            for x, c in enumerate(col):
                if (x, y) in self.cart_positions:
                    s += str(self.find_cart(x, y))
                else:
                    s += c
            s += '\n'
        return s[:-1]

    def __iter__(self):
        return self

    def __next__(self):
        if self.crash:
            return self
        self.carts = sorted(self.carts)
        self.check_for_collisions()
        self.drive_carts()
        self.remove_crashed_carts()
        return self

    @property
    def cart_positions(self):
        return [cart.pos for cart in self.carts]

    @property
    def final_cart(self):
        if len(self.carts) == 1:
            return self.carts[0].pos

    def other_carts(self, this_cart):
        return [cart for cart in self.carts if cart != this_cart]

    def other_carts_next_positions(self, this_cart):
        return [cart.next_pos for cart in self.other_carts(this_cart)]

    def check_for_collisions(self):
        for cart in self.carts:
            crash_1 = cart.next_pos in self.cart_positions
            crash_2 = cart.next_pos in self.other_carts_next_positions(cart)
            if crash_1:
                other_carts = [other_cart for other_cart in self.other_carts(cart)
                               if other_cart.pos == cart.next_pos]
            elif crash_2:
                other_carts = [other_cart for other_cart in self.other_carts(cart)
                               if other_cart.next_pos == cart.next_pos]
            if crash_1 or crash_2:
                self.crashed_carts.add(cart)
                self.crashed_carts.update(other_carts)

    def drive_carts(self):
        for cart in self.carts:
            next(cart)
            x, y = cart.pos
            if self.map[y, x] in '\\/':
                cart.corner(self.map[y, x])
            elif self.map[y, x] == '+':
                cart.intersection()

    def remove_crashed_carts(self):
        for cart in self.crashed_carts:
            if self.crash_mode:
                cart.c = 'X'
                self.crash = True
                self.crash_point = cart.pos
            else:
                self.carts.remove(cart)
        self.crashed_carts = set()

    def read_map(self, data):
        carts = '^>v<'
        w, h = len(data), len(data[0])
        self.map = np.empty((w, h), dtype=str)
        for y, col in enumerate(data):
            for x, c in enumerate(col):
                if c in carts:
                    self.carts.append(Cart(x, y, c))
                    track = self.replace_cart(c)
                    self.map[y, x] = track
                else:
                    self.map[y, x] = c

    def replace_cart(self, c):
        return {
            '^': '|',
            '>': '-',
            'v': '|',
            '<': '-',
        }[c]

    def find_cart(self, x, y):
        return self.carts[self.cart_positions.index((x, y))]

def read_test_data(file, size):
    with open(file) as f:
        data = f.read()
    return [d.split('\n')[:size] for d in data.split('\n\n')]

def read_data(file):
    with open(file) as f:
        return f.readlines()

# test part 1

test_data = read_test_data('test_data', size=6)
start = test_data.pop(0)
map = MineCartMap(start, crash_mode=True)

assert not map.crash
print(map)
assert str(map) == '\n'.join(start)
for td, m in zip(test_data, map):
    expected = '\n'.join(td)
    print("expecting:")
    print(expected)
    print("actual:")
    print(m)
    assert str(m) == expected
assert m.crash
assert m.crash_point == (7, 3)

print()
print("part 1")
print()

# part 1

data = read_data('input')
map = MineCartMap(data, crash_mode=True)
while not map.crash:
    next(map)
print(map)
print(map.crash_point)

# test part 2

print()
print("test 2")
print()

test_data = read_test_data('test_data_2', size=7)
start = test_data.pop(0)
map = MineCartMap(start)

print("expecting:")
print('\n'.join(start))
print("actual:")
print(map)
assert str(map) == '\n'.join(start)

for td, m in zip(test_data, map):
    expected = '\n'.join(td)
    print("expecting:")
    print(expected)
    print("actual:")
    print(m)
    assert str(m) == expected
assert m.final_cart == (6, 4)

# part 2

data = read_data('input')
map = MineCartMap(data)
while not map.final_cart:
    next(map)
print(map.final_cart)
