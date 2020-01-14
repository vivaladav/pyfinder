import astar
import sys

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print("USAGE: python {0} file.map".format(sys.argv[0]))
        sys.exit(1)

    f = open(sys.argv[1], 'r')
    fdata = f.readlines()
    f.close()

    # DEBUG
    for line in fdata:
        print(line, end='')
    print()

    mapRows = len(fdata)
    if(mapRows == 0):
        print("ERROR empty map")
        sys.exit(1)

    mapCols = len(fdata[0])

    r0 , c0 = (int(v) for v in tuple(input("START (a,b): ").split(',')))

    if(r0 < 0 or r0 >= mapRows or c0 < 0 or c0 >= mapCols):
        print("ERROR start is out of bounds")
        sys.exit(1)

    if(fdata[r0][c0] == '#'):
        print("ERROR start is not walkable")
        sys.exit(1)

    r1 , c1 = (int(v) for v in tuple(input("GOAL (a,b): ").split(',')))

    if(r1 < 0 or r1 >= mapRows or c1 < 0 or c1 >= mapCols):
        print("ERROR goal is out of bounds")
        sys.exit(1)

    if(fdata[r1][c1] == '#'):
        print("ERROR goal is not walkable")
        sys.exit(1)

    if(r0 == r1 and c0 == c1):
        print("ERROR start = goal")
        sys.exit(1)

    start = (r0, c0)
    goal = (r1, c1)

    pf = astar.Pathfinder(fdata)

    path = pf.make_path(start, goal)

    print()

    for r in range(mapRows):
        for c in range(mapCols):
            if((r, c) in path):
                if((r, c) == path[0]):
                    print('S', end='')
                elif((r, c) == path[len(path) - 1]):
                    print('X', end='')
                else:
                    print('.', end='')
            else:
                print(fdata[r][c], end='')

    print()
