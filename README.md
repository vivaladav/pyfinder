# pyfinder
An A* (A-star) pathfinder in Python.

I am creating this to learn more about Python and the plan is to create 3 applications using different libraries to handle things in different ways.

Because I am doing this for learning, I published this repository after the first commit, when nothing is finished yet. The idea is to share the whole progress with others and eventually to get feedback along the way.

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

![example of usage of pg-pyfinder.py](https://github.com/vivaladav/pyfinder/blob/master/data/docs/imgs/pg-pyfinder-01.png?raw=true)

Second parameter is optional and it defines the size of a cell of the map in pixels (default is 30).

To search for a path simply click on the map twice. After a path is visualized click one more time to clear it. 

### qt-pyfinder.py
A visual application based on Qt for Python.

**Current status:** under development

#### Example of usage
> $ python3 qt-pyfinder.py

## Map format
Currently a map is a text file which contains 2 possible symbols:
- **' '** = walkable cell
- **'#'** = unwalkable cell

Map cells start from (0, 0) which represents the first characer of the map file.

Examples of map files can be found in *data/maps/*
