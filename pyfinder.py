import astar
import sys

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

    # ask user for START
    r0 , c0 = (int(v) for v in tuple(input("START (a,b): ").split(',')))

    # ask user for GOAL
    r1 , c1 = (int(v) for v in tuple(input("GOAL (a,b): ").split(',')))

    start = (r0, c0)
    goal = (r1, c1)

    print()

    # find path
    pf = astar.Pathfinder(map)

    try:
        path = pf.make_path(start, goal)

    except astar.OutOfBoundsError as err:
        print("ERROR - {}".format(err))
        exit(1)
    except astar.UnwalkableError as err:
        print("ERROR - {}".format(err))
        exit(1)
    except astar.SameStartGoalError as err:
        print("ERROR - {}".format(err))
        exit(1)

    # print map with path
    pathStart = path[0]
    pathGoal = path[len(path) - 1]
    pathSet = set(path)

    for r in range(mapRows):
        for c in range(mapCols):
            if((r, c) in pathSet):
                if((r, c) == pathStart):
                    print('S', end='')
                elif((r, c) == pathGoal):
                    print('X', end='')
                else:
                    print('.', end='')
            else:
                if map[r][c] == 1:
                    print(' ', end='')
                else:
                    print('#', end='')
        print('\n', end='')

    print()
