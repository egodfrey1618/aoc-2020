import re
from functools import reduce

class Tile(object):
    def __init__(self, grid):
        self.grid = grid
        self.edge_N = self.grid[0]
        self.edge_S = self.grid[-1]
        self.edge_W = "".join(x[0] for x in self.grid)
        self.edge_E = "".join(x[-1] for x in self.grid)

    def all_orientations(self):
        # Generates a list of all of the possible rotations/etc. of the grid.
        tiles = [self]

        # Add on the rotations
        for i in range(3):
            tiles.append(tiles[-1].rotate())

        # Flip horizontally, and add in every rotation.
        tiles.append(self.flip_horiz())
        for i in range(3):
            tiles.append(tiles[-1].rotate())

        # Flip diagonally, and add in every rotation. 
        tiles.append(self.flip_diag())
        for i in range(3):
            tiles.append(tiles[-1].rotate())

        # Don't keep any duplicates.
        # TODO: I've done something wrong with my symmetries here. There should be 8 symmetries of the 
        # square, and I'm computing 12, so some of my "flip-and-rotate" ones are the same. I'm too tired
        # to figure out which ones though, and this works well enough.
        deduped_tiles = []
        seen_grids = set()
        for t in tiles:
            if "\n".join(t.grid) not in seen_grids:
                deduped_tiles.append(t)
                seen_grids.add("\n".join(t.grid))

        return deduped_tiles

    def rotate(self):
        grid = []
        grid_len = len(self.grid)
        for i in range(grid_len):
            grid.append("".join([self.grid[j][i] for j in range(grid_len-1, -1, -1)]))
        return Tile(grid)

    def flip_horiz(self):
        grid = ["".join(line[::-1]) for line in self.grid]
        return Tile(grid)

    def flip_diag(self):
        grid = []
        grid_len = len(self.grid)
        for i in range(grid_len):
            grid.append("".join([self.grid[j][i] for j in range(grid_len)]))
        return Tile(grid)

    def __repr__(self):
        return self.grid.__repr__()

all_tiles = {}
all_tile_ids = set()

# Read the tiles. We'll store them as a dictionary from (tile_id, orientation_id) to a Tile.
# The exact format of orientation_id doesn't matter for the rest of the code.
f = open("input")
while f:
    tile_line = f.readline().strip()
    if tile_line == "": break
    tile_id = int(re.findall("^Tile ([0-9]*):$", tile_line)[0])

    lines = []
    while (line := f.readline().strip()) != "":
        lines.append(line)
    tiles = Tile(lines).all_orientations()

    # Add these to our sets.
    for (i, tile) in enumerate(tiles):
        all_tiles[(tile_id, i)] = tile
    all_tile_ids.add(tile_id)

# Now parse out all of the edges - i.e. which (tile+rotation)s are allowed to be next to each other.
# We'll store this as a dictionary from (tile_id, rotation_id) to a 4-tuple of lists of valid neighbours.
#
# This is O(n^2) - it's possible to do this more efficiently, but I don't care, the number of tiles is small.
all_edges = {key : ([], [], [], []) for key in all_tiles.keys()}

for (key_1, tile_1) in all_tiles.items():
    for (key_2, tile_2) in all_tiles.items():
        if key_1[0] == key_2[0]:
            continue

        # See which edge scan line up.
        if tile_1.edge_N == tile_2.edge_S:
            all_edges[key_1][0].append(key_2)
        if tile_1.edge_S == tile_2.edge_N:
            all_edges[key_1][1].append(key_2)
        if tile_1.edge_W == tile_2.edge_E:
            all_edges[key_1][2].append(key_2)
        if tile_1.edge_E == tile_2.edge_W:
            all_edges[key_1][3].append(key_2)

# OK, an early optimisation - figure out which tiles MUST be on the border. We'll do this by
# seeing what the max number of neighbours a given tile_id could have.
best_connectivity = {}
for (key, edges) in all_edges.items():
    tile_id = key[0]
    this_orientation = len([x for x in edges if x])
    best_connectivity[tile_id] = max(this_orientation, best_connectivity.get(tile_id, 0))

# This wasn't guaranteed, but the puzzle maker was kind to us. (This also lets us solve Part 1, without 
# having to construct the whole grid yet!)
GRID_LENGTH = 12

corner_pieces = [k for k in all_tile_ids if best_connectivity[k] == 2]
assert len(corner_pieces) == 4

edge_pieces = [k for k in all_tile_ids if best_connectivity[k] == 3]
assert len(edge_pieces) == (4*GRID_LENGTH) - 8

print("Product of corner pieces:", reduce(lambda x, y: x*y, corner_pieces))

# OK, now let's actually solve the puzzle!
class State(object):
    """
    A partially filled in puzzle.
    """
    def __init__(self):
        self.grid = [[None for _ in range(GRID_LENGTH)] for _ in range(GRID_LENGTH)]

        # I started off with this complexity, but I'm pretty sure I don't need it, and can just keep track of which tile_ids are used.
        self.remaining_corner_pieces = set(corner_pieces)
        self.remaining_edge_pieces = set(edge_pieces)
        self.remaining_middle_pieces = set(x for x in all_tile_ids if x not in corner_pieces and x not in edge_pieces)

    def _categorise_position(self, position):
        def is_edge(x): return x == 0 or x == GRID_LENGTH - 1
        edges = len([p for p in position if is_edge(p)])
        if edges == 2:
            return "corner"
        elif edges == 1:
            return "edge"
        elif edges == 0:
            return "middle"
        assert False

    def possible_next_tiles(self, position):
        """
        Says what tiles are possible in a given position. Returns None if we haven't placed any tiles that would
        restrict this position.
        """
        def in_grid(p): 
            def f(x): return x >= 0 and x < GRID_LENGTH
            (x, y) = p
            return f(x) and f(y)

        position_type = self._categorise_position(position)
        if position_type == "corner":
            valid_tile_ids = self.remaining_corner_pieces
        elif position_type == "edge":
            valid_tile_ids = self.remaining_edge_pieces
        elif position_type == "middle":
            valid_tile_ids = self.remaining_middle_pieces
        else:
            assert False

        (x, y) = position
        # This is a bit gross - a bit of magic here with what the "directions" in the edges mean.
        neighbours = [((x-1, y), 1), ((x+1, y), 0), ((x, y-1), 3), ((x, y+1), 2)]
        possibilities = None
        for (n, direction) in neighbours:
            if in_grid(n) and (neighbour_tile := self.grid[n[0]][n[1]]) != None:
                valid_given_neighbour = all_edges[neighbour_tile][direction]
                if possibilities == None:
                    possibilities = set(valid_given_neighbour)
                else:
                    possibilities &= set(valid_given_neighbour)
        possibilities = [(tile_id, orientation_id) for (tile_id, orientation_id) in possibilities if tile_id in valid_tile_ids]
        return list(possibilities)

    def place_tile(self, position, tile):
        position_type = self._categorise_position(position)
        tile_id = tile[0]
        if position_type == "corner":
            self.remaining_corner_pieces.remove(tile_id)
        elif position_type == "edge":
            self.remaining_edge_pieces.remove(tile_id)
        elif position_type == "middle":
            self.remaining_middle_pieces.remove(tile_id)
        else:
            assert False

        self.grid[position[0]][position[1]] = tile

    def remove_tile(self, position):
        tile_id = self.grid[position[0]][position[1]][0]
        self.grid[position[0]][position[1]] = None

        position_type = self._categorise_position(position)
        if position_type == "corner":
            self.remaining_corner_pieces.add(tile_id)
        elif position_type == "edge":
            self.remaining_edge_pieces.add(tile_id)
        elif position_type == "middle":
            self.remaining_middle_pieces.add(tile_id)
        else:
            assert False

def solve_grid():
    # This is essentially a BFS which tries to fill in the puzzle. 
    # We keep track of our state in [State]. We also have a list that traces down the path through the recursion tree
    # so far, saying what remaining tiles we can try placing at each of the prior positions.
    #
    # Then all the backtracking, etc. is just contained inside this function. [State] deals with figuring out which tiles
    # are OK to place next. There are smarter things we could do in [State] to try and cut out some paths early, but this
    # runs fast enough.
    starting_tile_id = list(corner_pieces)[0]

    s = State()
    position = (0, 0)

    starting_tile_and_orientations = [k for k in all_tiles.keys() if k[0] == starting_tile_id]

    # recursion_path consists of nodes which are (position_number, tiles to try at this position)
    recursion_path = [(0, starting_tile_and_orientations)]

    # order of positions to try
    positions = []
    for i in range(GRID_LENGTH):
        positions.extend((i, j) for j in range(GRID_LENGTH))
    assert len(set(positions)) == GRID_LENGTH * GRID_LENGTH

    while recursion_path:
        # Loop invariant: At the start of this loop, we HAVEN'T placed this tile (yet)
        (position_idx, tiles) = recursion_path[-1]

        if tiles == []:
            # Wind back.
            recursion_path.pop()
            if recursion_path == []:
                # We're over. The grid is empty at this point, we couldn't fill it in.
                break
            (position_idx, _) = recursion_path[-1]
            position = positions[position_idx]
            s.remove_tile(position)
        else:
            position = positions[position_idx]
            (x, y) = position

            # Place this tile, and continue.
            tile = tiles.pop()
            s.place_tile(position, tile)
            next_position_idx = position_idx + 1
            if next_position_idx >= len(positions):
                # We've filled in every tile in the grid.
                print("filled in grid")
                return s
            else:
                next_position = positions[next_position_idx]
                tiles = s.possible_next_tiles(next_position)
                recursion_path.append((next_position_idx, tiles))

solved_state = solve_grid()

# OK, perfect! Now onto part 2.

# Reconstruct the grid into a single block, stripping out any borders.
l = []
for row in solved_state.grid:
    for i in range(1, len(all_tiles[row[0]].grid) - 1):
        l.append("".join(all_tiles[subtile].grid[i][1:-1] for subtile in row))

# And reuse the tile logic to get all orientations
all_orientations = [t.grid for t in Tile(l).all_orientations()]

SEA_MONSTER = [
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   "
]
sea_monster_dimensions = (len(SEA_MONSTER), len(SEA_MONSTER[0]))
sea_monster_spots = set()
for i, sea_monster_row in enumerate(SEA_MONSTER):
    for j, sea_monster_char in enumerate(SEA_MONSTER[i]):
        if sea_monster_char == "#": sea_monster_spots.add((i, j))

# Search for the monster
for grid in all_orientations:
    sea_monster_positions = []

    for row in range(0, len(grid) - sea_monster_dimensions[0]):
        for col in range(0, len(grid[0]) - sea_monster_dimensions[1]):
            if all(grid[row+i][col+j] == "#" for (i, j) in sea_monster_spots):
                sea_monster_positions.append((row, col))

    if sea_monster_positions == []:
        print("No sea monsters found at this orientation...")
        continue

    # Once we've found all the sea monsters, fill them in with stars
    grid = [list(row) for row in grid]

    for (row, col) in sea_monster_positions:
        for (i, j) in sea_monster_spots:
            grid[row+i][col+j] = "*"

    # And print how many #s there are left.
    print("".join(y for x in grid for y in x).count("#"))
