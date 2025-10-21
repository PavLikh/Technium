from collections import deque
class Node:
    def __init__(self, value: int):
        self.value = value

        self.outbound = []
        self.inbound = []

    def point_to(self, *others):
        for other in others:
            self.outbound.append(other)
            other.inbound.append(self)

    def __str__(self):
        return f'Node({self.value})'

class Graph:
    def __init__(self, root: Node):
        self._root = root
        self.stack = [] # для dfs

    def dfs(self, node: Node | None = None):
        if node in self.visited:
            return
        
        if node is None:
            node = self._root
            self.stack = self._root.outbound
            self.visited = set()
        else:
            self.stack = node.outbound

        print(node, end = ' ')
        self.visited.add(node)
        
        for neighbor in self.stack:
            self.dfs(neighbor)

    def bfs(self, node: Node | None = None):
        self.visited = set()
        self.queue = deque()
        if node is None:
            node = self._root

        self.queue.append(node)
        self.visited.add(node)

        while self.queue:
            vertex = self.queue.popleft()
            print(vertex, end = ' ')

            for neighbor in vertex.outbound:
                if neighbor not in self.visited:
                    self.queue.append(neighbor)
                    self.visited.add(neighbor)


start = Node(0)
one = Node(1)
two = Node(2)
three = Node(3)
four = Node(4)
start.point_to(one, two, three)
one.point_to(start, two)
two.point_to(start, one, four)
three.point_to(start)
four.point_to(two)
g = Graph(start)
print('BFS:')
g.bfs()
print("\nDFS:")
g.dfs()
print()
