# pyfinder
An A* (A-star) pathfinder in Python.

I am creating this to learn more about Python and the plan is to create 3 applications using different libraries to handle things in different ways.

Because I am doing this for learning, I published this repository after the first commit, when nothing is finished yet. The idea is to share the whole progress with others and eventually to get feedback along the way.

## Applications
### pyfinder.py
This is the first version of the pathfinder.
It's a CLI (Command Line Interface) application that loads a map from a file passed as argument, then prompts the user for a start and a goal cell and finally shows the path.

#### Current status
Under development

#### Example of usage
> $ python3 pyfinder.py data/maps/map_01.map

### pg-pyfinder.py
A visual application based on pygame.

#### Current status
TODO

### qt-pyfinder.py
A visual application based on Qt for Python.

#### Current status
TODO

## Map format
Currently a map is a text file which contains 2 possible symbols:
- **' '** = walkable cell
- **'#'** = unwalkable cell

Examples of map files can be found in *data/maps/* 
