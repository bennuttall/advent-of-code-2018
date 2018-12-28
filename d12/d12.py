from itertools import islice

def windowed(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield ''.join(result)
    for elem in it:
        result = result[1:] + (elem,)
        yield ''.join(result)

def get_input(file):
    with open(file) as inp:
        plants = inp.readline()[15:].strip()
        rules = [rule.replace(' => #\n', '')
                 for rule in inp.readlines()
                 if rule.endswith('#\n')]
    return plants, rules

plants = '#..#.#..##......###...###'

rules = [
    '...##',
    '..#..',
    '.#...',
    '.#.#.',
    '.#.##',
    '.##..',
    '.####',
    '#.#.#',
    '#.###',
    '##.#.',
    '##.##',
    '###..',
    '###.#',
    '####.',
]

expected = [
    '...#..#.#..##......###...###...........',
    '...#...#....#.....#..#..#..#...........',
    '...##..##...##....#..#..#..##..........',
    '..#.#...#..#.#....#..#..#...#..........',
    '...#.#..#...#.#...#..#..##..##.........',
    '....#...##...#.#..#..#...#...#.........',
    '....##.#.#....#...#..##..##..##........',
    '...#..###.#...##..#...#...#...#........',
    '...#....##.#.#.#..##..##..##..##.......',
    '...##..#..#####....#...#...#...#.......',
    '..#.#..#...#.##....##..##..##..##......',
    '...#...##...#.#...#.#...#...#...#......',
    '...##.#.#....#.#...#.#..##..##..##.....',
    '..#..###.#....#.#...#....#...#...#.....',
    '..#....##.#....#.#..##...##..##..##....',
    '..##..#..#.#....#....#..#.#...#...#....',
    '.#.#..#...#.#...##...#...#.#..##..##...',
    '..#...##...#.#.#.#...##...#....#...#...',
    '..##.#.#....#####.#.#.#...##...##..##..',
    '.#..###.#..#.#.#######.#.#.#..#.#...#..',
    '.#....##....#####...#######....#.#..##.',
]

class Plants:
    def __init__(self, plants, rules):
        self.live_plants = {i for i, p in enumerate(plants) if p == '#'}
        self.rules = rules

    def __str__(self):
        return ''.join('#' if i in self.live_plants else '.' for i in self.range)

    def __iter__(self):
        return self

    def __next__(self):
        self.live_plants = {i for i in self.extended_range
                       if self.slice(i) in self.rules}
        return self

    @property
    def range(self):
        return range(min(self.live_plants), max(self.live_plants) + 1)

    @property
    def extended_range(self):
        return range(min(self.live_plants) - 2, max(self.live_plants) + 3)

    def slice(self, mid):
        pots = range(mid - 2, mid + 3)  # ppPpp
        return ''.join('#' if i in self.live_plants else '.' for i in pots)

    def show(self, start, end):
        pots = range(start, end + 1)
        return ''.join('#' if i in self.live_plants else '.' for i in pots)

    def sum(self):
        return sum(self.live_plants)

plants = Plants(plants, rules)
exp = expected.pop(0)
assert plants.show(-3, 35) == exp
for exp, p in zip(expected, plants):
    assert p.show(-3, 35) == exp
assert plants.sum() == 325

plants, rules = get_input('input')

plants = Plants(plants, rules)
for i in range(20):
    next(plants)
print(plants.sum())

plants, rules = get_input('input')

plants = Plants(plants, rules)
last_sum = 0
last_diff = 0
n = 50000000000
for i in range(n):
    next(plants)
    new_sum = plants.sum()
    diff = new_sum - last_sum
    if diff == last_diff:
        print(plants.sum() + (n-i-1)*diff)
        break
    last_sum = new_sum
    last_diff = diff
