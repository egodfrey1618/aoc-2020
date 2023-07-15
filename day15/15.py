from collections import namedtuple

class State(object):
    def __init__(self, starting_numbers):
        self.last_times = {}
        self.second_last_times = {}
        for i,c in enumerate(starting_numbers):
            self.last_times[c] = i+1
        self.most_recent = starting_numbers[-1]
        self.turn = len(starting_numbers)

    def step(self):
        self.turn += 1

        # Figure out what number we're saying next.
        target = self.most_recent
        if target not in self.second_last_times:
            result = 0
        else:
            result = self.last_times[target] - self.second_last_times[target]

        # And say it, updating the dictionaries
        if result in self.last_times:
            self.second_last_times[result] = self.last_times[result]
        self.last_times[result] = self.turn
        self.most_recent = result

l = [6,19,0,5,7,13,1]
s = State(l)
while s.turn < 30_000_000:
    s.step()
    l.append(s.most_recent)
print(s.most_recent)

