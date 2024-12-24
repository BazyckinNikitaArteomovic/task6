from collections import deque

class Graph:
    def __init__(self, field):
        self.field = field
        self.rows = len(field)
        self.cols = len(field[0])
        self.adj_list = [[] for _ in range(self.rows * self.cols + 1)]
        self.sink_node = self.rows * self.cols
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for row in range(self.rows):
            for col in range(self.cols):
                if field[row][col] != 1:
                    v1 = row * self.cols + col
                    for dr, dc in self.directions:
                        vrow, vcol = row + dr, col + dc
                        if 0 <= vrow < self.rows and 0 <= vcol < self.cols:
                            if field[vrow][vcol] == 0:
                                v2 = vrow * self.cols + vcol
                                self.add_edge(v1, v2)

    def add_edge(self, v1, v2):
        if v2 not in self.adj_list[v1]:
            self.adj_list[v1].append(v2)

    def add_sink_edges(self, exits):
        for exit_node in exits:
            self.adj_list[exit_node].append(self.sink_node)

    def bfs(self, source, sink, parent):
        visited = [False] * (self.sink_node + 1)
        queue = deque([source])
        visited[source] = True

        while queue:
            u = queue.popleft()

            for v in self.adj_list[u]:
                if not visited[v]:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == sink:
                        return True

        return False

    def ford_fulkerson(self, source, sink):
        parent = [-1] * (self.sink_node + 1)
        max_flow = 0

        while self.bfs(source, sink, parent):
            path_flow = float('Inf')
            v = sink

            while v != source:
                u = parent[v]
                path_flow = min(path_flow, 1)
                v = u

            max_flow += path_flow

            v = sink
            while v != source:
                u = parent[v]
                self.adj_list[u].remove(v)
                self.adj_list[v].append(u)
                v = u

        return max_flow

    def find_source(self):
        for x in range(self.rows):
            for y in range(self.cols):
                if self.field[x][y] == 2:
                    return x * self.cols + y

    def find_exits(self):
        exits = []

        for col in range(self.cols):
            if self.field[0][col] == 0:
                exits.append(col)
            if self.field[self.rows - 1][col] == 0:
                exits.append((self.rows - 1) * self.cols + col)

        for row in range(self.rows):
            if self.field[row][0] == 0:
                exits.append(row * self.cols)
            if self.field[row][self.cols - 1] == 0:
                exits.append(row * self.cols + self.cols - 1)

        return exits

    def process(self):
        source = self.find_source()
        exits = self.find_exits()
        self.add_sink_edges(exits)
        return self.ford_fulkerson(source, self.sink_node)


field = [
    [0, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 0, 2, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0]
]
field2 = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

task = Graph(field)
task2 = Graph(field2)
print(task.process())
print(task2.process())