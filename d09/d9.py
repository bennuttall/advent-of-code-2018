from itertools import cycle
from collections import deque


class MarbleCircle:
    def __init__(self, maxlen):
        self.circle = deque([0], maxlen=maxlen)

    def __len__(self):
        return len(self.circle)

    def __eq__(self, other):
        copy = self.circle.copy()
        while copy[0] != 0:
            copy.rotate()
        return list(copy) == other

    def place(self, marble):
        self.circle.rotate(-1)
        self.circle.append(marble)

    @property
    def bonus(self):
        self.circle.rotate(7)
        bonus = self.circle.pop()
        self.circle.rotate(-1)
        return bonus

    @property
    def current_marble(self):
        return self.circle[-1]


class MarbleGame:
    def __init__(self, players, marbles):
        self.scores = {p: 0 for p in range(players)}
        self.players = cycle(self.scores)
        self.marbles = list(reversed(range(1, marbles+1)))
        self.circle = MarbleCircle(maxlen=marbles+1)

    def __next__(self):
        current_player = next(self.players)
        next_marble = self.marbles.pop()
        if next_marble % 23 == 0:
            bonus = self.circle.bonus
            self.scores[current_player] += next_marble + bonus
        else:
            self.circle.place(next_marble)

    @property
    def is_active(self):
        return len(self.marbles) > 0

    @property
    def high_score(self):
        return max(self.scores.values())

game = MarbleGame(players=9, marbles=25)
circle = game.circle
assert len(game.marbles) == 25
assert circle == [0]
assert game.circle.current_marble == 0
assert len(game.scores) == 9
assert sum(game.scores.values()) == 0
next(game)
assert len(game.marbles) == 24
assert circle == [0, 1]
assert game.circle.current_marble == 1
assert sum(game.scores.values()) == 0
next(game)
assert len(game.marbles) == 23
assert circle == [0, 2, 1]
assert game.circle.current_marble == 2
assert sum(game.scores.values()) == 0

game = MarbleGame(players=9, marbles=25)
for i in range(22):
    next(game)
assert sum(game.scores.values()) == 0
next(game)
assert game.scores[4] == 23 + 9

def test(players, marbles, score):
    game = MarbleGame(players, marbles)
    for i in range(marbles):
        next(game)
    assert game.high_score == score, game.scores

test(9, 25, 32)
test(10, 1618, 8317)
test(13, 7999, 146373)
test(17, 1104, 2764)
test(21, 6111, 54718)
test(30, 5807, 37305)

game = MarbleGame(players=473, marbles=70904)
while game.is_active:
    next(game)
print(game.high_score)

game = MarbleGame(players=473, marbles=70904*100)
while game.is_active:
    next(game)
print(game.high_score)
