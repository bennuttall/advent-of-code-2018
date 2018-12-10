test_data_1 = ["Step B must be finished before step A can begin."]

test_data = """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
"""[1:-1].split('\n')

with open('input') as inp:
    data = [line.strip() for line in inp.readlines()]

def create_dependency_dict(data):
    dependencies = {}
    for rule in data:
        a = rule[36]
        b = rule[5]
        if a not in dependencies:
            dependencies[a] = set()
        if b not in dependencies:
            dependencies[b] = set()
        dependencies[a].add(b)
    return dependencies

def order_steps(data):
    dependencies = create_dependency_dict(data)
    steps = []
    available_steps = set()
    while len(steps) < len(dependencies):
        for step, deps in dependencies.items():
            if step not in steps:
                if all(dep in steps for dep in deps):
                    available_steps.add(step)
        next_step = sorted(available_steps)[0]
        steps.append(next_step)
        available_steps.remove(next_step)

    return ''.join(steps)

assert order_steps(test_data_1) == 'BA'
assert order_steps(test_data) == 'CABDFE'
print(order_steps(data))
