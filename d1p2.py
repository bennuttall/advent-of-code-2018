from itertools import cycle

def calculate(data):
    f = 0
    fs = set([f])

    for d in cycle(data):
        f += d
        if f in fs:
            return f
        fs.add(f)

def test(data, expected):
    actual = calculate(data)
    assert actual == expected, actual

# tests
d = [1, -1]
test(d, 0)
d = [3, 3, 4, -2, -4]
test(d, 10)
d = [-6, +3, +8, +5, -6]
test(d, 5)
d = [7, 7, -2, -7, -4]
test(d, 14)

if __name__ == '__main__':
    from d1p1 import data

    print(calculate(data))
