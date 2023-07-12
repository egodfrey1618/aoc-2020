def manhattan_pos(pos):
    (x, y) = pos
    if x < 0: x *= -1
    if y < 0: y *= -1
    return x + y

class Ship1(object):
    def __init__(self):
        self.dir = "E"
        self.pos = (0, 0)

    def move(self, dir, z):
        if dir == "L" or dir == "R":
            # Rotate
            self._rotate(dir, z)
        else:
            # Move. If we're given forward, translate that to our direction first.
            dir = self.dir if dir == "F" else dir
            (x, y) = self.pos

            if dir == "E":
                self.pos = (x, y + z)
            elif dir == "W":
                self.pos = (x, y - z)
            elif dir == "N":
                self.pos = (x + z, y)
            elif dir == "S":
                self.pos = (x - z, y)
            else:
                assert False

    def _rotate(self, left_or_right, z):
        assert z % 90 == 0
        z //= 90 # How many steps.

        # Convenience functions - represent dirs as 0-3.
        def dir_to_n(dir): return "NESW".index(dir)
        def n_to_dir(n): return "NESW"[n]

        dir_n = dir_to_n(self.dir)
        dir_n += (z * (1 if left_or_right == "R" else -1))
        dir_n &= 0b11 # mod 4
        self.dir = n_to_dir(dir_n)

class Ship2(object):
    def __init__(self):
        self.dir = "E"
        self.ship_pos = (0, 0)
        self.waypoint_pos = (1, 10) # relative to the ship

    def move(self, dir, z):
        if dir == "L" or dir == "R":
            # Rotate the waypoint around the ship.
            # We'll calculate this as a number of rotations to the right we should do.
            assert z % 90 == 0
            z //= 90
            if dir == "L": z *= -1
            z &= 0b11
            for _ in range(z):
                self._rotate_waypoint_right()
        elif dir in "NESW":
            # Move the waypoint. This is duplicated a bunch with Ship1 - probably should
            # have abstracted out position / direction into a separate thing.
            (x, y) = self.waypoint_pos

            if dir == "E":
                self.waypoint_pos = (x, y + z)
            elif dir == "W":
                self.waypoint_pos = (x, y - z)
            elif dir == "N":
                self.waypoint_pos = (x + z, y)
            elif dir == "S":
                self.waypoint_pos = (x - z, y)
            else:
                assert False
        elif dir == "F":
            (x, y) = self.waypoint_pos
            (v, w) = self.ship_pos
            self.ship_pos = (v + z*x, w + z*y)
        else:
            assert False

    def _rotate_waypoint_right(self):
        # (1, 0) should go to (0, 1). (North to East)
        # (0, 1) should go to (-1, 0). (East to South)
        (x, y) = self.waypoint_pos
        self.waypoint_pos = (-1*y, x)

lines = open("input","r").read().strip().split("\n")
lines = [(line[0], int(line[1:])) for line in lines]

# Part 1
p = Ship1()
for (dir, z) in lines:
    p.move(dir, z)
print(manhattan_pos(p.pos))

# Part 2
p = Ship2()
for (dir, z) in lines:
    p.move(dir, z)
print(manhattan_pos(p.ship_pos))
