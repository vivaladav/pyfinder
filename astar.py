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

    def __init__(self, map = None):
        """
        Parameters
        ----------
        map : list
            list containing sub-lists reprenting the rows of the map
        """
        self.set_map(map)

        self.openList = []
        self.openMap = dict()
        self.closedMap = dict()
        self.goal = ()
        self.costHor = 10
        self.costDia = 14

    def set_map(self, map):
        self.map = map

        if map != None:
            self.mapRows = len(map)
            self.mapCols = len(map[0])
        else:
            self.mapRows = 0
            self.mapCols = 0

    def add_to_open(self, node, idx):
        """Add a node to the open list.

        Parameters
        ----------
        node : Node
            node to add to the open list
        idx : int
            unique index of the node in the map
        """
        heapq.heappush(self.openList, node)
        self.openMap[idx] = node

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

    def cost_to_adj(self, dr, dc):
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
        # if both deltas are 1 it's a diagonal cell
        if dr != 0 and dc != 0:
            return self.costDia
        else:
            return self.costHor

    def cost_to_goal(self, src):
        """Compute the approximated cost of moving from src cell to the goal using the Manhattan distance heuristic.

        Parameters
        ----------
        src : tuple
            row,col of the current cell

        Returns
        -------
        int
            approximated cost of movement to the goal cell
        """
        r0, c0 = src
        r1, c1 = self.goal
        return (abs(r0 - r1) + abs(c0 - c1)) * self.costHor

    def handle_node(self, prev, dr, dc):
        """Generate and process a neighbor node.

        Parameters
        ----------
        prev : Node
            predecessor node in the path, potentially its parent
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
        if(self.map[r][c] == 0):
            return

        adjIdx = self.cell_index(r, c)

        # in closed list
        if(adjIdx in self.closedMap):
            return

        adjG = self.cost_to_adj(dr, dc) + prev.g
        adjH = self.cost_to_goal((r, c))

        # in open list
        if(adjIdx in self.openMap):
            old = self.openMap[adjIdx]

            # new path has a better cost
            if(old.g > adjG):
                old.set_costs(adjG, adjH)
                old.parent = prev
                heapq.heapify(self.openList)

        # new node
        else:
            adj =  Node(r, c, adjG, adjH, prev)
            self.add_to_open(adj, adjIdx)

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

        # start out of bounds
        if(r0 < 0 or r0 >= self.mapRows or c0 < 0 or c0 >= self.mapCols):
            raise OutOfBoundsError(start)

        # goal out of bounds
        if(r1 < 0 or r1 >= self.mapRows or c1 < 0 or c1 >= self.mapCols):
            raise OutOfBoundsError(goal)

        # start is unwalkable
        if(self.map[r0][c0] == 0):
            raise UnwalkableError(start)

        # goal is unwalkable
        if(self.map[r1][c1] == 0):
            raise UnwalkableError(goal)

        # start == goal
        if(start == goal):
            raise SameStartGoalError(start)

        self.goal = goal

        self.openList = []
        self.openMap.clear()
        self.closedMap.clear()

        path = []

        # add start node to the open list
        s = Node(r0, c0, 0, self.cost_to_goal(start))
        self.add_to_open(s, self.cell_index(r0, c0))

        # process nodes in the open list
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

                # add start node
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

class OutOfBoundsError(Exception):
    """Exception raised when start or goal are outside the map."""

    def __init__(self, cell):
        """
        Parameters
        ----------
        cell : tuple
            row,col of the cell generating the error
        """
        self.cell = cell

    def __str__(self):
        return "Out of bound cell: {}".format(self.cell)

class UnwalkableError(Exception):
    """Exception raised when start or goal cells are unwalkable"""

    def __init__(self, cell):
        """
        Parameters
        ----------
        cell : tuple
            row,col of the cell generating the error
        """
        self.cell = cell

    def __str__(self):
        return "Unwalkable cell: {}".format(self.cell)

class SameStartGoalError(Exception):
    """Exception raised when start or goal cells are the same"""

    def __init__(self, cell):
        """
        Parameters
        ----------
        cell : tuple
            row,col of the cell generating the error
        """
        self.cell = cell

    def __str__(self):
        return "Same start and goal cell: {}".format(self.cell)
