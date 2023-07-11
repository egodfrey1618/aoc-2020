class Instruction(object):
    def __init__(self, s):
        (x, y) = s.split(" ")
        if x in ["nop", "acc", "jmp"]:
            self.command = x
        else:
            assert False, f"Unknown instruction: {x}"

        self.value = int(y)

class State(object):
    def __init__(self):
        self.acc = 0
        self.position = 0 

    def apply(self, instruction):
        if instruction.command == "nop":
            self.position += 1
            return None
        elif instruction.command == "acc":
            self.position += 1
            self.acc += instruction.value
            return None
        elif instruction.command == "jmp":
            self.position += instruction.value
            return None
        else:
            assert False

instructions = [Instruction(line) for line in open("input").read().strip().split("\n")]

def run_instructions(instructions):
    """
    Runs instructions until either we fall off the end or hit an infinite loop.
    """
    state = State()
    visited_states = set()
    while (position := state.position) not in visited_states and position >= 0 and position < len(instructions):
        visited_states.add(position)
        state.apply(instructions[position])
    return state

# Part 1
state = run_instructions(instructions)
print(state.acc)

# Part 2
for i in range(len(instructions)):
    # For each instruction, try changing jmp to nop, and rerunning.
    instruction = instructions[i]

    if instruction.command == "jmp":
        instruction.command = "nop"
        state = run_instructions(instructions)
        instruction.command = "jmp"
    elif instruction.command == "nop":
        instruction.command = "jmp"
        state = run_instructions(instructions)
        instruction.command = "nop"
    else:
        continue

    if state.position == len(instructions):
        print(state.acc)
