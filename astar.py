import heapq

class Node:
    """Data used by a Pathfinder to represent a single walkable cell."""

    def __init__(self, r, c, g = 0, h = 0, parent = None):
        """
        Parameters
        ----------
        r : int
            row of the cell
        c : int
            col of the cell
        g : int
            cost of path to this node
        h : int
            estimated cost from this node to goal
        parent : Node
            previous Node in the path
        """
        self.r = r
        self.c = c

        self.f = g + h
        self.g = g
        self.h = h

        self.parent = parent

    def set_costs(self, g, h):
        """Set G and H costs and compute F from them.

        Parameters
        ----------
        g : int
            cost of path to this node
        h : int
            estimated cost from this node to goal
        """
        self.f = g + h
        self.g = g
        self.h = h

    def __lt__(self, other):
        """Operator < required by heapq."""
        return self.f < other.f

class Pathfinder:
    """Pathfinder that implements the A* search in a map."""

    def __init__(self, map):
        """
        Parameters
        ----------
        map : list
            list containing sub-lists reprenting the rows of the map
        """
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
        """Get the index of a cell from its row and col.

        Parameters
        ----------
        r : int
            row of the cell
        c : int
            col of the cell

        Returns
        -------
        int
            an unique index identifying one cell of the map
        """
        return r * self.mapCols + c

    def adj_cost(self, dr, dc):
        """Compute the cost of moving to an adjacent cell.

        Parameters
        ----------
        dr : int
            row delta, it can be -1, 0, 1
        dc : int
            col delta, it can be -1, 0, 1

        Returns
        -------
        int
            cost of movement to the next cell
        """
        if(abs(dr) == 1 and abs(dc) == 1):
            return self.costDiag
        else:
            return self.costHori

    def dist_H(self, a, b):
        """Compute the approximated cost of moving from once cell to another using the Manhattan distance heuristic.

        Parameters
        ----------
        a : tuple
            row,col of the first cell
        b : tuple
            row,col of the second cell

        Returns
        -------
        int
            approximated cost of movement to the goal cell
        """
        r0, c0 = a
        r1, c1 = b
        return (abs(r0 - r1) + abs(c0 - c1)) * self.costHori

    def handle_node(self, prev, dr, dc):
        """Generate and process a neighbor node.

        Parameters
        ----------
        dr : int
            row delta, used to define the row of the new node. It can be -1, 0, 1
        dc : int
            col delta, used to define the col of the new node. It can be -1, 0, 1
        """
        r = prev.r + dr
        c = prev.c + dc

        # out of bounds
        if(r < 0 or r >= self.mapRows or c < 0 or c >= self.mapCols):
            return

        # not walkable
        if(self.map[r][c] == '#'):
            return

        adjIdx = self.cell_index(r, c)

        # in closed list
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
        """Implementation of the A* search.

        Parameters
        ----------
        start : tuple
            row,col of the start cell
        goal : tuple
            row,col of the destination cell

        Returns
        -------
        list
            all the (row, col) tuples making the path. First tuple is start and last one is goal.
        """
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

            # goal found -> generate path and return
            if(curr.r == r1 and curr.c == c1):
                while(curr.parent != None):
                    path.append((curr.r, curr.c))
                    curr = curr.parent

                path.append((curr.r, curr.c))

                path.reverse()

                return path

            # process neighbor nodes
            self.handle_node(curr, -1, -1)
            self.handle_node(curr, -1, 0)
            self.handle_node(curr, -1, 1)

            self.handle_node(curr, 0, -1)
            self.handle_node(curr, 0, 1)

            self.handle_node(curr, 1, -1)
            self.handle_node(curr, 1, 0)
            self.handle_node(curr, 1, 1)

        return path






