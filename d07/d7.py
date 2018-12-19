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

class TaskManager:
    def __init__(self, data):
        self.dependencies = create_dependency_dict(data)
        self.assigned = []
        self.done = []

    @property
    def complete(self):
        return len(self.done) == len(self.dependencies)

    @property
    def next_step(self):
        if len(self.assigned) < len(self.dependencies):
            available_steps = set()
            for step, deps in self.dependencies.items():
                if step not in self.assigned:
                    if all(dep in self.done for dep in deps):
                        available_steps.add(step)
            if available_steps:
                return sorted(available_steps)[0]

    def assign(self, step):
        self.assigned.append(step)

    def mark_done(self, step):
        self.done.append(step)

def worker_factory():
    return {
        'current_step': None,
        'finish_time': None,
    }

class Workforce:
    def __init__(self, data, n=1, base_task_time=0):
        self.manager = TaskManager(data)
        self.workers = [worker_factory() for i in range(n)]
        deps = sorted(self.manager.dependencies)
        self.task_times = {
            step: n
            for n, step in enumerate(deps, start=base_task_time + 1)
        }
        self.done = []
        self.time = 0

    def __next__(self):
        self.time += 1

    @property
    def complete(self):
        return self.manager.complete

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, time):
        self._time = time
        self.check_tasks()
        self.start_tasks()

    def start_tasks(self):
        for worker in self.workers:
            next_step = self.manager.next_step
            if worker['current_step'] is None and next_step:
                self.assign(worker, next_step)

    def assign(self, worker, step):
        finish_time = self.time + self.task_times[step]
        worker['current_step'] = step
        worker['finish_time'] = finish_time
        self.manager.assign(step)

    def check_tasks(self):
        for worker in self.workers:
            if self.time == worker['finish_time']:
                step = worker['current_step']
                self.done.append(step)
                self.manager.mark_done(step)
                worker['finish_time'] = None
                worker['current_step'] = None

assert order_steps(test_data_1) == 'BA'
assert order_steps(test_data) == 'CABDFE'

manager = TaskManager(test_data_1)
assert not manager.complete
assert manager.next_step == 'B'
manager.assign('B')
assert manager.next_step is None
manager.mark_done('B')
assert manager.next_step == 'A'
manager.assign('A')
assert manager.next_step is None
assert not manager.complete
manager.mark_done('A')
assert manager.next_step is None
assert manager.complete

manager = TaskManager(test_data)
assert not manager.complete
assert manager.next_step == 'C'
manager.assign('C')
assert manager.next_step is None
manager.mark_done('C')
assert manager.next_step == 'A'
manager.assign('A')
assert manager.next_step == 'F'
manager.assign('F')
manager.mark_done('A')
assert manager.next_step == 'B'
manager.assign('B')
manager.mark_done('B')
assert manager.next_step == 'D'
manager.assign('D')
manager.mark_done('F')
manager.mark_done('D')
assert manager.next_step == 'E'
manager.assign('E')
assert not manager.complete
manager.mark_done('E')
assert manager.complete

wf = Workforce(test_data, n=2)
w1, w2 = wf.workers
assert not wf.complete
assert wf.time == 0
assert w1['current_step'] == 'C'
assert w1['finish_time'] == 3, w1
assert w2['current_step'] is None
next(wf)
assert wf.time == 1
assert w1['current_step'] == 'C'
assert w2['current_step'] is None
next(wf)
assert wf.done == []
next(wf)
assert wf.time == 3
assert wf.done == ['C']
assert w1['current_step'] == 'A'
assert w2['current_step'] == 'F'
for i in range(12):
    assert not wf.complete
    next(wf)
assert wf.time == 15
assert wf.complete
assert wf.done == ['C', 'A', 'B', 'F', 'D', 'E']

wf = Workforce(test_data_1, base_task_time=10)
w = wf.workers[0]
assert wf.time == 0
for i in range(12):
    assert w['current_step'] == 'B'
    assert not wf.complete
    next(wf)
assert wf.time == 12
for i in range(11):
    assert w['current_step'] == 'A'
    assert not wf.complete
    next(wf)
assert wf.complete
assert wf.done == ['B', 'A']

print(order_steps(data))

wf = Workforce(data, n=5, base_task_time=60)
while not wf.complete:
    next(wf)
print(wf.time)
