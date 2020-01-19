import astar
import pygame
import sys

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

    # get size of map
    mapRows = len(map)
    mapCols = len(map[0])

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
    CELL_SIZE = 30
    if argc == 3:
        CELL_SIZE = int(sys.argv[2])
    print("Cell size: {0}x{1}".format(CELL_SIZE, CELL_SIZE))

    BORDER_SIZE = 1
    INCELL_SIZE = CELL_SIZE - (BORDER_SIZE * 2)

    COLOR_BG = (33, 33, 33)
    COLOR_WALK = (230, 230, 230)
    COLOR_UNWALK = (99, 99, 99)
    COLOR_START = (41, 182, 246)
    COLOR_GOAL = (0, 230, 118)
    COLOR_PATH = (255, 245, 157)
    COLOR_NOPATH = (239, 83, 80)

    mapW = mapCols * CELL_SIZE
    mapH = mapRows * CELL_SIZE
    mapX0 = int((winSize[0] - mapW) / 2)
    mapY0 = int((winSize[1] - mapH) / 2)
    mapX1 = mapX0 + mapW
    mapY1 = mapY0 + mapH

    win.fill(COLOR_BG, (mapX0, mapY0, mapW, mapH))

    for r in range(mapRows):
        cellY = mapY0 + (r * CELL_SIZE) + BORDER_SIZE

        for c in range(mapCols):
            cellX = mapX0 + (c * CELL_SIZE) + BORDER_SIZE

            col = (255, 0, 255)

            if(map[r][c] == 1):
                col = COLOR_WALK
            elif(map[r][c] == 0):
                col = COLOR_UNWALK

            win.fill(col, (cellX, cellY, INCELL_SIZE, INCELL_SIZE))

    pygame.display.flip()

    # init scene
    start = None
    goal = None

    pf = astar.Pathfinder(map)

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

                if event.button == 1:
                    posX = event.pos[0]
                    posY = event.pos[1]

                    if posX < mapX0 or posX > mapX1 or posY < mapY0 or posY > mapY1:
                        continue

                    # set start
                    if start == None:
                        start = (int((event.pos[1] - mapY0) / CELL_SIZE), int((event.pos[0] - mapX0) / CELL_SIZE))

                        if map[start[0]][start[1]] == 1:
                            startX = mapX0 + (start[1] * CELL_SIZE) + BORDER_SIZE
                            startY = mapY0 + (start[0] * CELL_SIZE) + BORDER_SIZE

                            win.fill(COLOR_START, (startX, startY, INCELL_SIZE, INCELL_SIZE))
                            pygame.display.flip()
                        else:
                            start = None

                    # set goal
                    elif goal == None:
                        goal = (int((event.pos[1] - mapY0) / CELL_SIZE), int((event.pos[0] - mapX0) / CELL_SIZE))

                        if map[goal[0]][goal[1]] == 1 and start != goal:
                            goalX = mapX0 + (goal[1] * CELL_SIZE) + BORDER_SIZE
                            goalY = mapY0 + (goal[0] * CELL_SIZE) + BORDER_SIZE

                            win.fill(COLOR_GOAL, (goalX, goalY, INCELL_SIZE, INCELL_SIZE))
                            pygame.display.flip()

                            try:
                                path = pf.make_path(start, goal)

                                if len(path) > 0:
                                    pathIdx = 1
                                    animating = True
                                else:
                                    win.fill(COLOR_NOPATH, (startX, startY, INCELL_SIZE, INCELL_SIZE))
                                    win.fill(COLOR_NOPATH, (goalX, goalY, INCELL_SIZE, INCELL_SIZE))
                                    pygame.display.flip()

                            except:
                                print("ERROR")
                        else:
                            goal = None

                    # clear everything
                    else:
                        start = None
                        goal = None
                        pathIdx = -1
                        animCounter = 0

                        if len(path) > 0:
                            for cell in path:
                                cellX = mapX0 + (cell[1] * CELL_SIZE) + BORDER_SIZE
                                cellY = mapY0 + (cell[0] * CELL_SIZE) + BORDER_SIZE

                                win.fill(COLOR_WALK, (cellX, cellY, INCELL_SIZE, INCELL_SIZE))
                        else:
                            win.fill(COLOR_WALK, (startX, startY, INCELL_SIZE, INCELL_SIZE))
                            win.fill(COLOR_WALK, (goalX, goalY, INCELL_SIZE, INCELL_SIZE))

                        pygame.display.flip()

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
                if animCounter == FRAMES_TO_SKIP:
                    cell = path[pathIdx]

                    cellX = mapX0 + (cell[1] * CELL_SIZE) + BORDER_SIZE
                    cellY = mapY0 + (cell[0] * CELL_SIZE) + BORDER_SIZE

                    win.fill(COLOR_PATH, (cellX, cellY, INCELL_SIZE, INCELL_SIZE))
                    pygame.display.flip()

                    pathIdx += 1
                    animCounter = 0
                else:
                    animCounter += 1
            else:
                animating = False

        # frame delay
        pygame.time.wait(30)
