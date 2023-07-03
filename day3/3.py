grid = []
with open("input","r") as f:
    for line in f:
        grid.append(line.strip())
width = len(grid[0])
assert all(len(x) == width for x in grid)

def add(x, y):
    z = (x[0] + y[0], x[1] + y[1])
    return z

def get_grid(position):
    return grid[position[0]][position[1]]

def in_grid(position):
    return position[0] < len(grid)

def how_many_trees_if_we_go_in_direction(direction):
    position = (0, 0)
    
    trees = 0
    while True:
        # Move
        position = add(position, direction)
        position = (position[0], position[1] % width)
    
        # Check if we're out of the grid
        if not in_grid(position):
            break
    
        # Check tree
        if get_grid(position) == "#":
            trees += 1
    return trees

directions = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
trees = [how_many_trees_if_we_go_in_direction(dir) for dir in directions]
print(trees)

# And print the product!
x = 1
for t in trees: x *= t
print(x)
