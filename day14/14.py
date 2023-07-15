import re
import itertools

class State(object):
    def __init__(self, version):
        self.mask = ""
        self.memory = {} 
        self.version = version
    
    def set_mask(self, mask):
        self.mask = mask

    def _apply_mask_basic(self, n):
        # Applies mask to a value, returns it.
        for i, c in enumerate(reversed(self.mask)):
            if c == "X": 
                pass
            elif c == "0":
                n &= ((2**36 - 1) - (2**i)) # AND with 0b11111....10111111
            elif c == "1":
                n |= 2**i # OR with 0b10000000
            else:
                assert False
        return n

    def _apply_mask_complex(self, n):
        # Applies mask. Return a generator of all possible values matching the mask.
        # I checked that masks contain max 9 X's, so this should be OK.

        x_positions = []

        # Get rid of the 0s and 1s first.
        for i, c in enumerate(reversed(self.mask)):
            if c == "0": 
                # nothing to do
                pass
            elif c == "X":
                # keep track of the position, we'll sort the Xs out below
                x_positions.append(i)
            elif c == "1":
                n |= 2**i # OR with 0b10000000
            else: assert False

        # And then loop through all possible mask values
        for mask_values in itertools.product([0, 1], repeat=len(x_positions)):
            new_n = n
            for (i, value) in zip(x_positions, mask_values):
                if value == 0:
                    new_n &= ((2**36 - 1) - (2**i)) # AND with 0b11111....10111111
                elif value == 1:
                    new_n |= 2**i # OR with 0b10000000
                else: assert False
            yield new_n

    def set_memory(self, location, value):
        if self.version == 1:
            value = self._apply_mask_basic(value)
            self.memory[location] = value
        elif self.version == 2:
            for location in self._apply_mask_complex(location):
                self.memory[location] = value

    def sum_memory_values(self):
        return sum(self.memory.values())

state1 = State(1)
state2 = State(2)

for line in open("input"):
    mask = re.findall("mask = ([01X]+)$", line)
    if mask:
        mask = mask[0]
        state1.set_mask(mask)
        state2.set_mask(mask)
        continue

    mem = re.findall("mem\[([0-9]+)\] = ([0-9]+)$", line)
    if mem:
        (location, value) = mem[0]
        location = int(location)
        value = int(value)
        state1.set_memory(location, value)
        state2.set_memory(location, value)

print(state1.sum_memory_values())
print(state2.sum_memory_values())
