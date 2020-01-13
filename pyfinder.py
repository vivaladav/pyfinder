import sys

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print("USAGE: python {0} file.map".format(sys.argv[0]))
        sys.exit(1)

    print("opening {0}\n".format(sys.argv[1]))

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

    # DEBUG
    print("map size: {0}x{1}\n".format(mapRows, mapCols))

    # DEBUG
    for line in fdata:
        for c in line:
            if(c == '#'):
                print('0', end='')
            elif(c == ' '):
                print('1', end='')
            elif(c == '\n'):
                print('\n', end='')
    print()

    r0 , c0 = (int(v) for v in tuple(input("START (a,b): ").split(',')))

    if(r0 < 0 or r0 >= mapRows or c0 < 0 or c0 >= mapCols):
        print("ERROR start is out of bounds")
        sys.exit(1)

    if(fdata[r0][c0] == '#'):
        print("ERROR start is not walkable")
        sys.exit(1)

    r1 , c1 = (int(v) for v in tuple(input("END (a,b): ").split(',')))

    if(r1 < 0 or r1 >= mapRows or c1 < 0 or c1 >= mapCols):
        print("ERROR end is out of bounds")
        sys.exit(1)

    if(fdata[r1][c1] == '#'):
        print("ERROR end is not walkable")
        sys.exit(1)

    if(r0 == r1 and c0 == c1):
        print("ERROR start = end")
        sys.exit(1)

    # DEBUG
    print("start {0},{1}".format(r0, c0))
    print("end {0},{1}".format(r1, c1))
