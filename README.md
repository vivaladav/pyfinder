# pyfinder
An A* (A-star) pathfinder in Python.

I am creating this to learn more about Python and the plan is to create 3 applications using different libraries to handle things in different ways.

I also added a simple benchmark to test how quick the pathfinder can be.

Because I am doing this for learning, I published this repository after the first commit, when nothing was finished yet. The idea is to share the whole progress with others and eventually to get feedback along the way.

Currently all the applications are feature complete and seem to work fine. Feel free to create an issue if you spot any bug or if you want to request a new feature.

## Applications
### pyfinder.py
This is the first version of the pathfinder.
It's a CLI (Command Line Interface) application that loads a map from a file passed as argument, then prompts the user for a start and a goal cell and finally shows the path.

**Current status:** Done

#### Example of usage
> $ python3 pyfinder.py data/maps/map_01.map

![example of usage of pyfinder.py](https://github.com/vivaladav/pyfinder/blob/master/data/docs/imgs/pyfinder-shell-01.png?raw=true)

### pg-pyfinder.py
A visual application based on pygame.

**Current status:** Done

#### Example of usage
> $ python3 pg-pyfinder.py data/maps/map_01.map 60

Second parameter is optional and it defines the size of a cell of the map in pixels (default is 30).

To search for a path simply click on the map twice.

![example of usage of pg-pyfinder.py](https://github.com/vivaladav/pyfinder/blob/master/data/docs/imgs/pg-pyfinder-01.png?raw=true)

After a path is visualized click one more time to clear it.

In the following image you can see what happens when no path can be found:

![example of pg-pyfinder when no path can be found](https://github.com/vivaladav/pyfinder/blob/master/data/docs/imgs/pg-pyfinder-02.png?raw=true)

### qt-pyfinder.py
A visual application based on Qt for Python.

**Current status:** Done

#### Example of usage
> $ python3 qt-pyfinder.py

After starting the application load a map from the menu *File > Open Map*:

![qt-pyfinder.py file menu](https://github.com/vivaladav/pyfinder/blob/master/data/docs/imgs/qt-pyfinder-01.png?raw=true)

It's possible to configure several options from the menu *File > Options*:

![qt-pyfinder.py options dialog](https://github.com/vivaladav/pyfinder/blob/master/data/docs/imgs/qt-pyfinder-02.png?raw=true)


### pyfinder-bench.py
A simple benchmark to verify how quick pathfinding is, on average.

**Current status:** Done

#### Example of usage
> $ python3 pyfinder-bench.py data/maps/map_01.map

![example of usage of pyfinder-bench.py](https://github.com/vivaladav/pyfinder/blob/master/data/docs/imgs/pyfinder-bench-shell-01.png?raw=true)

## Map format
Currently a map is a text file which contains 2 possible symbols:
- **' '** = walkable cell
- **'#'** = unwalkable cell

Map cells start from (0, 0) which represents the first characer of the map file.

Examples of map files can be found in *data/maps/*
