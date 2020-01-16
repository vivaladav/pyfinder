import astar
import pygame
import sys

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print("USAGE: python {0} file.map".format(sys.argv[0]))
        sys.exit(1)

    # read map
    with open(sys.argv[1], 'r') as f:
        fdata = f.readlines()

    map = []
    for line in fdata:
        # strip '\n' at the end
        map.append(line[0 : len(line) -1])

    # get size of map
    mapRows = len(map)

    if(mapRows == 0):
        print("ERROR empty map")
        sys.exit(1)

    mapCols = len(map[0])

    # set up pygame
    pygame.init()

    # screen info
    screenInfo = pygame.display.Info()
    print("Screen size: {0}x{1}".format(screenInfo.current_w, screenInfo.current_h))

    # set up window
    winSize = (960, 540)
    win = pygame.display.set_mode(winSize)

    # render map
    CELL_SIZE = 30
    BORDER_SIZE = 1
    INCELL_SIZE = CELL_SIZE - (BORDER_SIZE * 2)

    BG_COLOR = (33, 33, 33)
    WALK_COLOR = (242, 242, 242)
    UNWALK_COLOR = (99, 99, 99)

    mapW = mapCols * CELL_SIZE
    mapH = mapRows * CELL_SIZE
    mapX = int((winSize[0] - mapW) / 2)
    mapY = int((winSize[1] - mapH) / 2)

    win.fill(BG_COLOR, (mapX, mapY, mapW, mapH))

    for r in range(mapRows):
        cellY = mapY + (r * CELL_SIZE) + BORDER_SIZE

        for c in range(mapCols):
            cellX = mapX + (c * CELL_SIZE) + BORDER_SIZE

            col = (255, 0, 255)

            if(map[r][c] == ' '):
                col = WALK_COLOR
            elif(map[r][c] == '#'):
                col = UNWALK_COLOR

            win.fill(col, (cellX, cellY, INCELL_SIZE, INCELL_SIZE))

    pygame.display.flip()

    # -- GAME LOOP --
    running = True

    while running:
        # handle events
        for event in pygame.event.get():
            # window closed
            if event.type == pygame.QUIT:
                running = False
            # key released
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # render
