import numpy as np
from operator import itemgetter
from pprint import pprint

size = 300

def get_power_level(x, y, serial):
    rack_id = x + 10
    foo = ((rack_id * y) + serial) * rack_id
    return int(str(foo)[-3]) - 5

def get_power_level_grid(serial):
    grid = np.zeros((size, size), dtype=np.int32)
    for x in range(size):
        for y in range(size):
            grid[x,y] = get_power_level(x+1, y+1, serial)
    return grid

def find_largest_square(grid, n):
    squares = {}
    for x in range(size - (n - 1)):
        for y in range(size - (n - 1)):
            squares[(x, y)] = grid[x:x+n,y:y+n].sum()
    largest = max(squares.items(), key=itemgetter(1))
    (x, y), largest_sum = largest
    return (x+1, y+1, largest_sum)

def find_largest_square_any_size(serial):
    grid = get_power_level_grid(serial)
    largest_squares = {n+1: find_largest_square(grid, n + 1) for n in range(size)}
    largest = max(largest_squares.items(), key=lambda e: e[1][2])
    n, (x, y, largest_sum) = largest
    return (x, y, n, largest_sum)

assert get_power_level(3, 5, 8) == 4
assert get_power_level(122, 79, 57) == -5
assert get_power_level(217, 196, 39) == 0
assert get_power_level(101, 153, 71) == 4

grid = get_power_level_grid(18)
assert find_largest_square(grid, 3) == (33, 45, 29)
grid = get_power_level_grid(42)
assert find_largest_square(grid, 3) == (21, 61, 30)

grid = get_power_level_grid(8199)
print(find_largest_square(grid, 3)[:2])

assert find_largest_square_any_size(18) == (90, 269, 16, 113)
assert find_largest_square_any_size(42) == (232, 251, 12, 119)

print(find_largest_square_any_size(8199))
