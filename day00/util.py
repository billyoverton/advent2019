import math

# From https://github.com/mcpower/adventofcode/blob/15ae109bc882ca688665f86e4ca2ba1770495bb4/utils.py
def min_max(l):
    return min(l), max(l)

# From https://stackoverflow.com/a/39644726
def get_digit(number, n):
    return number // 10**n % 10

def init_grid(height, width, fill=None):
    grid = [[]] * (height)
    for y in range(height):
        grid[y] = [fill]*width
    return grid

def pretty_grid(array, xsep="", ysep="\n"):
    string_list = []
    for y in array:
        string_list.append(xsep.join([str(i) for i in y]))
    return ysep.join(string_list)

def between(x, a, b):
    return (a <= x <= b) or (b <= x <= a)

def to_unit_vector(vector):
    unit = []
    magnitude = math.sqrt( sum([x**2 for x in vector]) )
    for x in vector:
        unit.append(x/magnitude)
    return unit

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def from_iterable(point):
        return Point(point[0], point[1])

    def distance(self, other):
        return math.sqrt( (self.x - other.x)**2 + (self.y - other.y)**2 )

    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def to_tuple(self):
        return (self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __str__(self):
        return "({0},{1})".format(self.x, self.y)

    def __hash__(self):
        return self.__str__().__hash__()

class Graph(object):

    def __init__(self):
        self.verticies = { }

    def add_vertex(self, vertex):
        if vertex not in self.vertices:
            self.verticies[vertex] = [ ]

    def add_edge(self, edge, weight=1, bidirectional=True):

        if edge[0] in self.verticies:
            self.verticies[edge[0]].append((edge[1],weight))
        else:
            self.verticies[edge[0]] = [ (edge[1],weight) ]

        if edge[1] not in self.verticies:
            self.verticies[edge[1]] = []

        if bidirectional:
            self.verticies[edge[1]].append( (edge[0],weight) )

    def neighbors(self, vertex):
        if vertex in self.verticies:
            return [x[0] for x in self.verticies[vertex]]
        else:
            return None

    def edge_weight(self, edge):
        if edge[0] not in self.verticies or edge[1] not in self.verticies:
            return None

        edges = self.verticies[edge[0]]
        for e in edges:
            if e[0] == edge[1]:
                return e[1]
        return None

    def dijkstra(self, source):
        if source not in self.verticies:
            return None

        verticies = set(self.verticies.keys())

        distance = { vertex:math.inf for vertex in verticies }
        previous = { vertex:None for vertex in verticies }
        distance[source] = 0

        while(len(verticies) > 0):
            distance_subset = { vertex:distance[vertex] for vertex in verticies }
            v = min(distance_subset, key=distance_subset.get)
            verticies.remove(v)

            for neighbor in [x for x in self.neighbors(v) if x in verticies]:
                new_distance = distance[v] + self.edge_weight([v,neighbor]) # Add weight
                if new_distance < distance[neighbor]:
                    distance[neighbor] = new_distance
                    previous[neighbor] = v

        return distance, previous

    def __str__(self):
        graph_str = []
        for vertex in self.verticies:
            graph_str.append(f'{vertex}: {self.verticies[vertex]}')
        return "\n".join(graph_str)
