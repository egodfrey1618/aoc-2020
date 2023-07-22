from collections import deque

f = open("input")
assert f.readline() == "Player 1:\n"
deck1 = []
while (line := f.readline().strip()) != "":
    deck1.append(int(line))
assert f.readline() == "Player 2:\n"
deck2 = []
while (line := f.readline().strip()) != "":
    deck2.append(int(line))

# Part 1
def play_part1(deck1, deck2):
    deck1 = deque(deck1)
    deck2 = deque(deck2)

    while deck1 and deck2:
        card1 = deck1.popleft()
        card2 = deck2.popleft()
        if card1 > card2:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)

    return deck1 if deck1 else deck2

winning_deck = play_part1(deck1, deck2)
total = 0
for i, c in enumerate(reversed(winning_deck)):
    total += (i+1) * c
print(total)

# Part 2
def play_part2(deck1, deck2):
    # Deques aren't really as good for this, at least in Python, as random access in a deque isn't O(n).
    # Ah well. Hopefully complexity doesn't matter for this part.
    seen_states = set()

    while deck1 and deck2:
        state = tuple(deck1 + [","] + deck2)
        if state in seen_states:
            # We've hit a repeated state
            return (1, deck1)
        else:
            seen_states.add(state)

        card1 = deck1.pop(0)
        card2 = deck2.pop(0)
        if card1 <= len(deck1) and card2 <= len(deck2):
            # Both have the ability to continue. RECURSE!
            winner, _deck = play_part2(deck1[:card1], deck2[:card2])
        else:
            winner = 1 if card1 > card2 else 2

        if winner == 1:
            deck1.append(card1)
            deck1.append(card2)
        elif winner == 2:
            deck2.append(card2)
            deck2.append(card1)
        else:
            assert False

    return (1, deck1) if deck1 else (2, deck2)

_winning_player, winning_deck = play_part2(deck1, deck2)
total = 0
for i, c in enumerate(reversed(winning_deck)):
    total += (i+1) * c
print(total)
