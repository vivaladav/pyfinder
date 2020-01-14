import heapq

class Node:
    def __init__(self, r, c, g = 0, h = 0, parent = None):
        self.r = r
        self.c = c

        self.f = g + h
        self.g = g
        self.h = h

        self.parent = parent

    def set_costs(self, g, h):
        self.f = g + h
        self.g = g
        self.h = h

    def __lt__(self, other):
        return self.f < other.f

    def __str__(self):
        return "Node f: {0} - g: {1} - h: {2}".format(self.f, self.g, self.h)

class Pathfinder:
    def __init__(self, map):
        self.map = map
        self.mapRows = len(map)
        self.mapCols = len(map[0])
        self.openList = []
        self.openMap = dict()
        self.closedMap = dict()
        self.start = ()
        self.goal = ()
        self.costHori = 10
        self.costDiag = 14

    def cell_index(self, r, c):
        return r * self.mapCols + c

    def dist_G(self, a, b):
        r0, c0 = a
        r1, c1 = b
        return abs(r0 - r1) + abs(c0 - c1)

    def adj_cost(self, dr, dc):
        if(abs(dr) == 1 and abs(dc) == 1):
            return self.costDiag
        else:
            return self.costHori

    def dist_H(self, a, b):
        r0, c0 = a
        r1, c1 = b
        return (abs(r0 - r1) + abs(c0 - c1)) * self.costHori

    def handle_node(self, prev, dr, dc):
        r = prev.r + dr
        c = prev.c + dc

        # out of bounds
        if(r < 0 or r >= self.mapRows or c < 0 or c >= self.mapCols):
            return

        # not walkable
        if(self.map[r][c] == '#'):
            return

        adjIdx = self.cell_index(r, c)

        # in closedd list
        if(adjIdx in self.closedMap):
            return

        adjG = self.adj_cost(dr, dc) + prev.g
        adjH = self.dist_H((r, c), self.goal)

        # in open list
        if(adjIdx in self.openMap):
            old = self.openMap[adjIdx]

            if(old.g > adjG):
                old.set_costs(adjG, adjH)
                heapq.heapify(self.openList)
                old.parent = prev

        # new node
        else:
            adj =  Node(r, c, adjG, adjH, prev)

            heapq.heappush(self.openList, adj)
            self.openMap[adjIdx] = adj

    def make_path(self, start, goal):
        r0, c0 = start
        r1, c1 = goal

        self.start = start
        self.goal = goal

        s = Node(r0, c0, 0, self.dist_H(start, goal))

        self.openList = []
        heapq.heappush(self.openList, s)

        self.openMap.clear()
        self.openMap[self.cell_index(r0, c0)] = s

        self.closedMap.clear()

        path = []

        while(len(self.openList) > 0):
            curr = heapq.heappop(self.openList)
            currIdx = self.cell_index(curr.r, curr.c)
            del self.openMap[currIdx]

            self.closedMap[currIdx] = curr

            if(curr.r == r1 and curr.c == c1):
                while(curr.parent != None):
                    path.append((curr.r, curr.c))
                    curr = curr.parent

                path.append((curr.r, curr.c))

                path.reverse()

                return path

            self.handle_node(curr, -1, -1)
            self.handle_node(curr, -1, 0)
            self.handle_node(curr, -1, 1)

            self.handle_node(curr, 0, -1)
            self.handle_node(curr, 0, 1)

            self.handle_node(curr, 1, -1)
            self.handle_node(curr, 1, 0)
            self.handle_node(curr, 1, 1)

        return path






