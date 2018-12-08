from itertools import zip_longest
from collections import namedtuple
from pprint import pprint
import operator
import better_exceptions
better_exceptions.hook()

Record = namedtuple('Record', ['month', 'day', 'hour', 'minute', 'message'])

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def get_record_from_line(r):
    return Record(int(r[6:8]), int(r[9:11]), int(r[12:14]), int(r[15:17]), r[19:])

def process_guard_records(records):
    if not records:
        return
    shift_start = records.pop(0)
    guard_id = int(shift_start.message.split('#')[1].split(' ')[0])
    guard_shifts[guard_id] = guard_shifts.get(guard_id, 0) + 1
    if guard_id not in guard_sleeps:
        guard_sleeps[guard_id] = {}
    for a, b in grouper(records, 2):
        assert a.message == 'falls asleep' and b.message == 'wakes up'
        assert (a.month, a.day, a.hour) == (b.month, b.day, b.hour)
        assert a.minute < b.minute
        asleep = range(a.minute, b.minute)
        for m in asleep:
            guard_sleeps[guard_id][m] = guard_sleeps[guard_id].get(m, 0) + 1

def sleepy_guard(data):
    records = [get_record_from_line(r) for r in data]
    guard_records = []
    for r in records:
        if r.message.startswith('Guard #'):
            process_guard_records(guard_records)
            guard_records = [r]
        else:
            guard_records.append(r)
    process_guard_records(guard_records)

    guard_sleep_counts = {k: (sum(v.values())) for k, v in guard_sleeps.items()}

    most_asleep_guard = max(guard_sleep_counts.items(),
                            key=operator.itemgetter(1))[0]

    most_asleep_guard_sleep_minutes = guard_sleeps[most_asleep_guard]
    most_asleep_minute = max(most_asleep_guard_sleep_minutes.items(),
                             key=operator.itemgetter(1))[0]

    most_often_asleep_minutes = [(g, max(s.items(), key=operator.itemgetter(1)))
                                  for g, s in guard_sleeps.items() if s]

    most_often_asleep_guard = max(
        most_often_asleep_minutes, key=lambda e: e[1][1]
    )

    return (
        most_asleep_guard * most_asleep_minute,
        most_often_asleep_guard[0] * most_often_asleep_guard[1][0]
    )

test_data = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up""".split('\n')

guard_sleeps = {}
guard_shifts = {}
assert sleepy_guard(test_data) == (240, 4455)

with open('input') as inp:
    data = sorted(line.strip() for line in inp.readlines())

guard_sleeps = {}
guard_shifts = {}
print(sleepy_guard(data))
