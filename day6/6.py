import string

groups = [s.split("\n") for s in open("input","r").read().strip().split("\n\n")]

# One-liners, because I feel like it.

# Part 1
print(sum(len(set("".join(group))) for group in groups))

# Part 2
print(sum(len([x for x in set("".join(group)) if all(x in y for y in group)]) for group in groups))
