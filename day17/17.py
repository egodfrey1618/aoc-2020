import itertools

class State(object):
    def __init__(self, slice_str, dimension):
        self._cubes = set()
        self._dimension = dimension

        for i, line in enumerate(slice_str.split("\n")):
            for j, c in enumerate(line):
                if c == "#":
                    cube_pos = tuple([i, j] + [0] * (dimension - 2))
                    self._cubes.add(cube_pos)

    def neighbour_cubes(self, cube):
        for move in itertools.product([-1, 0, 1], repeat=self._dimension):
            # Skip the move that's all zeroes.
            if all(x == 0 for x in move): continue

            next_cube = tuple(x+y for (x, y) in zip(cube, move))
            yield next_cube

    def evolve(self):
        # Count cells and how many "marks" they have - i.e. neighbouring cells that are active.
        marks = {}

        for cube in self._cubes:
            for neighbour_cube in self.neighbour_cubes(cube):
                marks[neighbour_cube] = marks.get(neighbour_cube, 0) + 1
   
        # Remove cubes that don't have 2 or 3 neighbours.
        cubes_to_remove = []
        for cube in self._cubes:
            if cube not in marks or marks[cube] not in [2, 3]:
                cubes_to_remove.append(cube)
        for cube in cubes_to_remove:
            self._cubes.remove(cube)

        # Add cubes that have 3 neighbours.
        for cube, mark_count in marks.items():
            if mark_count == 3:
                self._cubes.add(cube)

s = open("input").read().strip()
state_3d = State(s, 3)
state_4d = State(s, 4)

for _ in range(6): 
    state_3d.evolve()
    state_4d.evolve()
print(len(state_3d._cubes))
print(len(state_4d._cubes))
