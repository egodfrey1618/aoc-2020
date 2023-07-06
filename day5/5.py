def is_power_of_2(x):
    if x < 0: return False

    while x > 1:
        if x & 1 != 0: return False
        x //= 2
    return True

class Range(object):
    def __init__(self, lower, upper):
        # Inclusive, exclusive
        self.lower = lower 
        self.upper = upper
        assert is_power_of_2(upper - lower)

    def cut_to_lower(self):
        mid = (self.lower + self.upper) // 2
        self.upper = mid

    def cut_to_upper(self):
        mid = (self.lower + self.upper) // 2
        self.lower = mid

    def singleton(self):
        return (self.upper - self.lower) == 1

def parse_seat(code):
    row = Range(0, 128)
    col = Range(0, 8)
    for c in code:
        if c == "F":
            row.cut_to_lower()
        elif c == "B":
            row.cut_to_upper()
        elif c == "L":
            col.cut_to_lower()
        elif c == "R":
            col.cut_to_upper()
        else:
            assert False, f"unknown char: {c}"
    assert row.singleton()
    assert col.singleton()
    return (row.lower, col.lower)

def seat_id(seat):
    return 8*seat[0] + seat[1]

lines = open("input","r").read().strip().split("\n")
seats = [parse_seat(line) for line in lines]
ids = [seat_id(seat) for seat in seats]
print(max(ids))

# Find my seat!
min_, max_ = min(ids), max(ids)
ids_set = set(ids)
for p in range(min_, max_):
    if p-1 in ids_set and p+1 in ids_set and p not in ids_set:
        print(p)
