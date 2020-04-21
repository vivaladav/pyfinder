import astar
import sys
import time

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print("USAGE: python {0} file.map".format(sys.argv[0]))
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        fdata = f.readlines()

    # print map
    for line in fdata:
        print(line, end='')
    print()

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

    # find walkable cells
    walkCells = []
    cellsNeeded = 224

    for r in range(mapRows):
        for c in range(mapCols):
            if(map[r][c] == 1):
                walkCells.append((r, c))
                cellsNeeded = cellsNeeded - 1

                if cellsNeeded == 0:
                    break

        if cellsNeeded == 0:
            break

    numPaths = len(walkCells) * (len(walkCells) - 1)

    print("Going to benchmark {} paths...\n".format(numPaths))

    # benchmark map
    pf = astar.Pathfinder(map)

    t0 = time.clock_gettime(time.CLOCK_THREAD_CPUTIME_ID)

    for start in walkCells:
        for goal in walkCells:
            if(start != goal):
                path = pf.make_path(start, goal)

    t1 = time.clock_gettime(time.CLOCK_THREAD_CPUTIME_ID)

    benchTime = t1 - t0
    avgPathTime = benchTime * 1000 / numPaths


    print("{:3.3} sec. to find {} paths".format(benchTime, numPaths))
    print("Average time per path: {:3.3} ms.\n".format(avgPathTime))
