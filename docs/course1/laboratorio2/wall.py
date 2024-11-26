from typing import Callable
from pytamaro import Graphic, Color
from pytamaro import rectangle, overlay

# error messages
from error_messages import arguments_error_message, CastleType

from color_functions import set_value, get_value
from brick_border import add_brick_borders

# constants
from measurements import wall_side_cm, pix_per_cm


### the wall function

def wall(color: Color, borders: bool, texture: Callable[[float, Color], Graphic]) -> Graphic:
    # ensure that the first parameter is a color
    assert isinstance(color, Color), arguments_error_message(wall, 0, CastleType.COLOR)
    # ensure that the first parameter is a wall border
    assert isinstance(borders, bool), arguments_error_message(wall, 1, CastleType.WALL_BORDER)
    # ensure that the third parameter is a wall property
    assert isinstance(texture, Callable), arguments_error_message(wall, 2, CastleType.WALL_PROPERTY)


    height = wall_side_cm * pix_per_cm
    width = wall_side_cm * pix_per_cm
    brick_height = height / 15
    brick_color = set_value(color, get_value(color) * 0.85)
    # plain wall
    result = rectangle(width, height, color)
    # add borders
    if borders:
        result = add_brick_borders(
            result, brick_height, brick_color,
            True, True
        )
    # add texture
    return overlay(
        texture(width, color),
        result
    )