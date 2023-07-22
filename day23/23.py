class Node(object):
    def __init__(self, value):
        self.value = value
        self.next = None

class State(object):
    # The state of the game, stored as:
    # - A singly linked list, which has a cycle.
    # - A dictionary from value to list.
    # 
    # So we can do a move in O(1) time - easy for us to find the place to insert the chunk.
    def __init__(self, values):
        self.nodes_by_value = {}
        self.start = None

        last_node = None
        for v in values:
            n = Node(v)
            if last_node:
                last_node.next = n
            if not self.start:
                self.start = n
            last_node = n
            self.nodes_by_value[v] = n

        last_node.next = self.start

    def move(self):
        chunk_node1 = self.start.next
        chunk_node2 = chunk_node1.next
        chunk_node3 = chunk_node2.next
        chunk_values = [node.value for node in (chunk_node1, chunk_node2, chunk_node3)]

        # Break the chunk out. 
        self.start.next = chunk_node3.next
        chunk_node3.next = None

        destination_cup = self.start.value
        while destination_cup == self.start.value or destination_cup in chunk_values:
            destination_cup -= 1
            if destination_cup not in self.nodes_by_value:
                destination_cup = max(self.nodes_by_value.keys())

        # And add the chunk back in!
        target_node = self.nodes_by_value[destination_cup]
        chunk_node3.next = target_node.next
        target_node.next = chunk_node1

        # And move the start around
        self.start = self.start.next

    def get_from_1(self, n):
        result = []
        node = self.nodes_by_value[1]
        for _ in range(n):
            node = node.next
            result.append(node.value)
        return result

l = [7,9,2,8,4,5,1,3,6]
s = State(l.copy())

# Part 1
for _ in range(100):
    s.move()
print("Solution to part 1", s.get_from_1(8))

# Part 2
l.extend(range(10, 1_000_001))
s = State(l)
for i in range(10_000_000):
    if i % 10_000 == 0: print(i)
    s.move()
X = s.get_from_1(2)
print("Solution to part 2", X[0] * X[1])
