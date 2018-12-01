with open('input.txt') as inp:
    data = inp.readlines()

data = [int(s.strip()) for s in data]

def calculate(data):
    return sum(data)

# tests
d = [1, 1, 1]
assert calculate(d) == 3
d = [1, 1, -2]
assert calculate(d) == 0
d = [-1, -2, -3]
assert calculate(d) == -6

if __name__ == '__main__':
    print(calculate(data))
