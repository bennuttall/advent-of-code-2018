test_data_raw = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"

def sum_tree(data):
    nc = data.pop(0)
    nm = data.pop(0)
    return sum(sum_tree(data) for i in range(nc)) + sum(data.pop(0) for i in range(nm))

def tree_value(data):
    nc = data.pop(0)
    nm = data.pop(0)
    values = [tree_value(data) for i in range(nc)]
    metadata = [data.pop(0) for i in range(nm)]
    if nc == 0:
        return sum(metadata)
    return sum(values[i-1] for i in metadata if i-1 in range(nc))

test_data = [int(d) for d in test_data_raw.split(' ')]
assert sum_tree(test_data) == 138
test_data = [int(d) for d in test_data_raw.split(' ')]
assert tree_value(test_data) == 66

with open('input') as inp:
    data = [int(d) for d in inp.readline().split(' ')]
print(sum_tree(data))
with open('input') as inp:
    data = [int(d) for d in inp.readline().split(' ')]
print(tree_value(data))
