def move(pos, d):
    (x, y) = pos
    if d == "e":
        (v, w) = (1, 0)
    elif d == "w":
        (v, w) = (-1, 0)
    elif d == "ne":
        (v, w) = (0, 1)
    elif d == "sw":
        (v, w) = (0, -1)
    elif d == "nw":
        (v, w) = (-1, 1)
    elif d == "se":
        (v, w) = (1, -1)
    else:
        assert False
    return (x+v, y+w)

def find_tile(s):
    pos = (0, 0)
    i = 0
    while i < len(s):
        c = s[i]
        if c == "e" or c == "w":
            # Single characters
            pos = move(pos, c)
            i += 1
        elif c == "n" or c == "s":
            # Double characters
            pos = move(pos, s[i:i+2])
            i += 2
        else:
            assert False
    return pos

# Part 1: Find the starting position.
black_tiles = set()
for line in open("input"):
    line = line.strip()
    tile = find_tile(line)
    black_tiles ^= {tile}
print(len(black_tiles))

# Part 2: Do the Conway moves.
for _ in range(100):
    marks = {}
    for tile in black_tiles:
        for d in ["e", "w", "nw", "ne", "sw", "se"]:
            new_tile = move(tile, d)
            marks[new_tile] = marks.get(new_tile, 0) + 1

    new_black_tiles = set()
    for tile, mark_count in marks.items():
        if tile not in black_tiles and mark_count == 2:
            new_black_tiles.add(tile)
        elif tile in black_tiles and mark_count in [1,2]:
            new_black_tiles.add(tile)
    black_tiles = new_black_tiles
    print(len(black_tiles))


