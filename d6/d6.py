import numpy as np
from scipy.spatial.distance import cityblock
import operator

test_locations = {
    'A': (1, 1),
    'B': (1, 6),
    'C': (8, 3),
    'D': (3, 4),
    'E': (5, 5),
    'F': (8, 9),
}

test_output = """
aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf
"""[1:-1]  # remove starting and trailing \n

class Map:
    def __init__(self, locations, case=False):
        self.locations = locations
        self.case = case
        self.construct_map()

    def __str__(self):
        s = ''
        for row in self.map:
            for i in row:
                s += i
            s += '\n'
        return s[:-1]

    def construct_map(self):
        coords = self.locations.values()
        max_x = max(coords, key=operator.itemgetter(0))[0]
        max_y = max(coords, key=operator.itemgetter(1))[1]
        max_xy = max(max_x, max_y) + 1

        self.map = np.zeros((max_xy, max_xy), str)
        for x in range(max_xy):
            for y in range(max_xy):
                self.map[y, x] = self.find_closest_location(x, y)

    def find_closest_location(self, x, y):
        closest, second_closest = sorted([
            (p, cityblock([x, y], [xi, yi]))
            for (p, (xi, yi)) in self.locations.items()
        ], key=operator.itemgetter(1))[:2]
        if closest[1] == second_closest[1]:
            return '.'
        ch = closest[0]
        if self.case:
            return ch if (x, y) in self.locations.values() else ch.lower()
        return ch

    @property
    def finite_locations(self):
        edges = (self.map[:,0], self.map[:,-1], self.map[0,:], self.map[-1,:])
        if self.case:
            infinite_locations = {ch.upper() for edge in edges for ch in edge} - set('.')
        else:
            infinite_locations = {ch for edge in edges for ch in edge} - set('.')
        return [loc for loc in self.locations if loc not in infinite_locations]

    @property
    def finite_areas(self):
        return {
            loc: str(self).upper().count(loc)
            for loc in self.finite_locations
        }

    @property
    def largest_finite_area(self):
        return max(self.finite_areas.items(), key=operator.itemgetter(1))[1]

map = Map(test_locations, case=True)
assert str(map) == test_output
assert map.finite_locations == ['D', 'E']
assert map.finite_areas == {'D': 9, 'E': 17}
assert map.largest_finite_area == 17

with open('input') as inp:
    data = [line.strip().split(', ') for line in inp.readlines()]
    coords = [(int(x), int(y)) for (x, y) in data]
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-=_+[]{};:@#<>"
    locations = {char: pos for char, pos in zip(chars, coords)}

map = Map(locations)
print(map.largest_finite_area)
