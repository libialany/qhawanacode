# premade walls
from castle_components import wall
from colors import grey, cyan, red, pink
from wall_borders import borders
from wall_properties import nothing, door, crack, ivy, bricks

plain_wall = wall(grey, borders, nothing)
entrance = wall(red, borders, door)
icy_wall = wall(cyan, borders, crack)
magical_wall = wall(pink, borders, ivy)


# premade battlements
from castle_components import battlement
from merlons import rectangular_merlon, split_merlon

simple_battlement = battlement(grey, rectangular_merlon)
magical_battlement = battlement(pink, split_merlon)


# to avoid errors if people have old versions and not reset cells
from castle_components import drawbridge