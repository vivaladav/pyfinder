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

    mapRows = len(fdata)
    if(mapRows == 0):
        print("ERROR empty map")
        sys.exit(1)

    mapCols = len(fdata[0])

    # ask user for START
    r0 , c0 = (int(v) for v in tuple(input("START (a,b): ").split(',')))

    # ask user for GOAL
    r1 , c1 = (int(v) for v in tuple(input("GOAL (a,b): ").split(',')))

    start = (r0, c0)
    goal = (r1, c1)

    print()

    # find path
    pf = astar.Pathfinder(fdata)

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
                print(fdata[r][c], end='')

    print()
