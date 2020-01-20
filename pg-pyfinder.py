import astar
import pygame
import sys

class VisualTilemap:
    """A 2D map made of tiles that can be rendered using pygame."""

    def __init__(self, cellSize, win, map):
        """
        Parameters
        ----------
        cellSize : int
            size of a cell of the map
        win : pygame.Surface
            target surface for rendering
        map : list
            map made of 0 and 1 representing walkable and unwalkable cells
        """
        self.SIZE_CELL = cellSize
        self.SIZE_BORDER = 1
        self.SIZE_INCELL = self.SIZE_CELL - (self.SIZE_BORDER * 2)

        self.win = win
        self.winW, self.winH = win.get_size()

        self.map = map
        self.mapRows = len(map)
        self.mapCols = len(map[0])

        self.mapW = self.mapCols * self.SIZE_CELL
        self.mapH = self.mapRows * self.SIZE_CELL
        self.mapX0 = int((self.winW - self.mapW) / 2)
        self.mapY0 = int((self.winH - self.mapH) / 2)
        self.mapX1 = self.mapX0 + self.mapW
        self.mapY1 = self.mapY0 + self.mapH

    def is_cell_walkable(self, cell):
        """Check if a cell is walkable.

        Parameters
        ----------
        cell : tuple
            row, col that define a cell of the map

        Returns
        -------
        bool
            True if the cell is walkable, False otherwise
        """
        r, c = cell
        return map[r][c] == 1

    def is_point_inside(self, point):
        """Check if a point is inside the map.

        Parameters
        ----------
        point : tuple
            x, y coordinates

        Returns
        -------
        bool
            True if the point is inside the map, False otherwise
        """
        x, y = point
        return x > self.mapX0 and x < self.mapX1 and y > self.mapY0 and y < self.mapY1

    def get_cell_from_point(self, point):
        """Return the cell corresponding to a point in the map.

        Parameters
        ----------
        point : tuple
            x, y coordinates

        Returns
        -------
        tuple
            row, col that define a cell of the map
        """
        x, y = point
        return (int((y - self.mapY0) / self.SIZE_CELL), int((x - self.mapX0) / self.SIZE_CELL))

    def drawMap(self, colorBg, colorWalk, colorUnwalk):
        """Draw the whole map, including background and all cells.

        Parameters
        ----------
        colorBg : tuple
            color to use for the background
        colorWalk : tuple
            color to use for all walkable cells
        colorUnwalk : tuple
            color to use for all unwalkable cells
        """
        win.fill(colorBg, (self.mapX0, self.mapY0, self.mapW, self.mapH))

        for r in range(self.mapRows):
            cellY = self.mapY0 + (r * self.SIZE_CELL) + self.SIZE_BORDER

            for c in range(self.mapCols):
                cellX = self.mapX0 + (c * self.SIZE_CELL) + self.SIZE_BORDER

                if(map[r][c] == 1):
                    win.fill(colorWalk, (cellX, cellY, self.SIZE_INCELL, self.SIZE_INCELL))
                elif(map[r][c] == 0):
                    win.fill(colorUnwalk, (cellX, cellY, self.SIZE_INCELL, self.SIZE_INCELL))

    def drawCell(self, cell, color):
        """Draw the inner part of a cell (no border).

        Parameters
        ----------
        cell : tuple
            row, col that define a cell of the map
        colorBg : tuple
            color to use for the cell
        """
        cellX = self.mapX0 + (cell[1] * self.SIZE_CELL) + self.SIZE_BORDER
        cellY = self.mapY0 + (cell[0] * self.SIZE_CELL) + self.SIZE_BORDER

        self.win.fill(color, (cellX, cellY, self.SIZE_INCELL, self.SIZE_INCELL))

if __name__ == "__main__":
    argc = len(sys.argv)

    if argc != 2 and argc != 3:
        print("USAGE: python {0} file.map [CELL_SIZE]".format(sys.argv[0]))
        sys.exit(1)

    # read map file
    with open(sys.argv[1], 'r') as f:
        fdata = f.readlines()

    # convert map file to usable format
    # 1 = walkable cell
    # 0 = unwalkable cell
    fRows = len(fdata)

    if(fRows == 0):
        print("ERROR empty map")
        sys.exit(1)

    # skip last column of '\n'
    fCols = len(fdata[0]) - 1

    map = []

    for r in range(fRows):
        map.append([1] * fCols)

    for r in range(fRows):
        for c in range(fCols):
            if(fdata[r][c] == '#'):
                map[r][c] = 0

    # set up pygame
    pygame.init()

    # screen info
    screenInfo = pygame.display.Info()
    print("Screen size: {0}x{1}".format(screenInfo.current_w, screenInfo.current_h))

    # set up window
    winSize = (1280, 720)
    win = pygame.display.set_mode(winSize)
    pygame.display.set_caption("PG-PYFINDER")
    print("Window size: {0}x{1}".format(winSize[0], winSize[1]))

    # render map
    sizeCell = 30
    if argc == 3:
        sizeCell = int(sys.argv[2])
    print("Cell size: {0}x{1}".format(sizeCell, sizeCell))

    COLOR_BG = (33, 33, 33)
    COLOR_WALK = (230, 230, 230)
    COLOR_UNWALK = (99, 99, 99)
    COLOR_START = (41, 182, 246)
    COLOR_GOAL = (0, 230, 118)
    COLOR_PATH = (255, 245, 157)
    COLOR_NOPATH = (239, 83, 80)

    vmap = VisualTilemap(sizeCell, win, map)

    vmap.drawMap(COLOR_BG, COLOR_WALK, COLOR_UNWALK)
    pygame.display.flip()

    # init scene
    pf = astar.Pathfinder(map)

    start = None
    goal = None
    pathIdx = -1
    animating = False
    animCounter = 0
    FRAMES_TO_SKIP = 4

    # -- GAME LOOP --
    running = True

    while running:
        # handle events
        for event in pygame.event.get():
            # mouse click
            if event.type == pygame.MOUSEBUTTONUP:
                # do not process more input during animation
                if animating:
                    continue

                # left click
                if event.button == 1:
                    if not vmap.is_point_inside(event.pos):
                        continue

                    # set start
                    if start == None:
                        start = vmap.get_cell_from_point(event.pos)

                        if vmap.is_cell_walkable(start):
                            vmap.drawCell(start, COLOR_START)
                            pygame.display.flip()
                        else:
                            start = None

                    # set goal
                    elif goal == None:
                        goal = vmap.get_cell_from_point(event.pos)

                        if vmap.is_cell_walkable(goal) and start != goal:
                            vmap.drawCell(goal, COLOR_GOAL)

                            try:
                                path = pf.make_path(start, goal)

                                # path found -> start animation
                                if len(path) > 0:
                                    pathIdx = 1
                                    animating = True
                                # no path found
                                else:
                                    vmap.drawCell(start, COLOR_NOPATH)
                                    vmap.drawCell(goal, COLOR_NOPATH)

                            except:
                                print("ERROR")

                            pygame.display.flip()
                        else:
                            goal = None

                    # clear everything
                    else:
                        if len(path) > 0:
                            for cell in path:
                                vmap.drawCell(cell, COLOR_WALK)
                        else:
                            vmap.drawCell(start, COLOR_WALK)
                            vmap.drawCell(goal, COLOR_WALK)

                        pygame.display.flip()

                        start = None
                        goal = None
                        pathIdx = -1
                        animCounter = 0

            # window closed
            elif event.type == pygame.QUIT:
                running = False

            # key released
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # render
        if animating:
            if pathIdx > 0 and pathIdx < (len(path) - 1):
                # poor man's animation skipping frames for fixed delay
                if animCounter == FRAMES_TO_SKIP:
                    cell = path[pathIdx]

                    vmap.drawCell(cell, COLOR_PATH)
                    pygame.display.flip()

                    pathIdx += 1
                    animCounter = 0
                else:
                    animCounter += 1
            else:
                animating = False

        # frame delay
        pygame.time.wait(30)
