def is_occupied_seat(grid, x, y):
    if x < 0 or x >= len(grid):
        return False
    if y < 0 or y >= len(grid[0]):
        return False
    c = grid[x][y]
    if c == ".":
        return False
    if c == "L":
        return False
    if c == "#":
        return True
    assert False

def evolve(grid, seat_to_marker_seats, number_to_clear_seat):
    """
    Evolve by one step.

    seat_to_marker_seat -> given a seat, says which seats we check to decide if we should flip it.
    number_to_clear_seat -> how many full seats cause a seat to become empty.
    """
    changed_seats = []

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == ".":
                # Nothing to do.
                continue

            marker_seats = seat_to_marker_seats[(x, y)]
            number_of_adjacent_full_seats = len([(x, y) for (x, y) in marker_seats if is_occupied_seat(grid, x, y)])

            if grid[x][y] == "L" and number_of_adjacent_full_seats == 0:
                changed_seats.append((x, y, "#"))
            if grid[x][y] == "#" and number_of_adjacent_full_seats >= number_to_clear_seat:
                changed_seats.append((x, y, "L"))

    for (x, y, c) in changed_seats:
        grid[x][y] = c
    return len(changed_seats)

# Part 1.
# This ends up taking a while - around 2.5s. Not thrilled by this, but it'll do!
grid = open("input").read().strip().split("\n")
grid = [list(x) for x in grid] 
seat_to_marker_seats = {}
for x in range(len(grid)):
    for y in range(len(grid[0])):
        adjacent_seats = [(x+d, y+e) for d in range(-1, 2) for e in range(-1, 2) if d != 0 or e != 0]
        seat_to_marker_seats[(x, y)] = adjacent_seats # includes some non-existent seats, but whatever.

while True:
    x = evolve(grid, seat_to_marker_seats, 4)
    if x == 0: 
        break
print(sum(s.count("#") for s in grid))

# Part 2.
grid = open("input").read().strip().split("\n")
grid = [list(x) for x in grid] 
seat_to_marker_seats = {}
for x in range(len(grid)):
    for y in range(len(grid[0])):
        directions = [(d, e) for d in range(-1, 2) for e in range(-1, 2) if d != 0 or e != 0]
        marker_seats = []
        for (d, e) in directions:
            (x1, y1) = (x, y)
            while (x2 := x1 + d) >= 0 and x2 < len(grid) and (y2 := y1 + e) >= 0 and y2 < len(grid[0]):
                (x1, y1) = (x2, y2)
                if grid[x1][y1] != ".": 
                    break
            if grid[x1][y1] == "." or (x1, y1) == (x, y):
                # We didn't find any seats in this direction at all. 
                continue
            elif grid[x1][y1] == "L":
                # We've hit our seat.
                marker_seats.append((x1, y1))
            else:
                # All points should be . or L to start with.
                assert False
        seat_to_marker_seats[(x, y)] = marker_seats
while True:
    x = evolve(grid, seat_to_marker_seats, 5)
    if x == 0: 
        break
print(sum(s.count("#") for s in grid))
