from itertools import cycle

class MarbleCircle:
    def __init__(self):
        self.circle = [0]
        self.current_marble = 0

    def __len__(self):
        return len(self.circle)

    def __getitem__(self, i):
        return self.circle[i % len(self.circle)]

    def place(self, marble):
        i = (self.circle.index(self.current_marble) + 1) % len(self) + 1
        self.circle.insert(i, marble)

    @property
    def bonus(self):
        bonus_pos = (self.circle.index(self.current_marble) - 7) % len(self)
        return (bonus_pos, self.circle.pop(bonus_pos))


class MarbleGame:
    def __init__(self, players, marbles):
        self.scores = [0] * players
        self.players = cycle(range(players))
        self.marbles = list(reversed(range(1, marbles+1)))
        self.circle = MarbleCircle()

    def __next__(self):
        self.current_player = next(self.players)
        next_marble = self.marbles.pop()
        if next_marble % 23 == 0:
            bonus_pos, bonus = self.circle.bonus
            self.scores[self.current_player] += next_marble + bonus
            next_marble = self.circle[bonus_pos]
        else:
            self.circle.place(next_marble)
        self.circle.current_marble = next_marble

    @property
    def is_active(self):
        return len(self.marbles) > 0

    @property
    def high_score(self):
        return max(self.scores)

game = MarbleGame(players=9, marbles=25)
circle = game.circle.circle
assert len(game.marbles) == 25
assert circle == [0]
assert game.circle.current_marble == 0
assert len(game.scores) == 9
assert sum(game.scores) == 0
next(game)
assert len(game.marbles) == 24
assert circle == [0, 1]
assert game.circle.current_marble == 1
assert sum(game.scores) == 0
next(game)
assert len(game.marbles) == 23
assert circle == [0, 2, 1]
assert game.circle.current_marble == 2
assert sum(game.scores) == 0

game = MarbleGame(players=9, marbles=25)
for i in range(22):
    next(game)
assert sum(game.scores) == 0
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
