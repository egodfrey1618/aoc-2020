import re

def parse_line(line):
    # Example: "1-3 a: abcde"
    matches = re.findall("^([0-9]*)-([0-9]*) (.): (.*)$", line)
    assert len(matches) == 1
    (lower, upper, char, password) = matches[0]
    lower = int(lower)
    upper = int(upper)
    return (lower, upper, char, password)

def validate_part1(lower, upper, char, password):
    count = password.count(char)
    return count >= lower and count <= upper

def validate_part2(lower, upper, char, password):
    c = password[lower-1]
    d = password[upper-1]

    if char not in [c, d]:
        return False
    if c == d: return False
    return True

lines = open("input","r").read().strip().split("\n")

def count(validate):
    count = 0
    for line in lines:
        (lower, upper, char, password) = parse_line(line)
        if validate(lower, upper, char, password):
            count += 1
    return count

print(count(validate_part1))
print(count(validate_part2))
