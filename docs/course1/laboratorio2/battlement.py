from typing import Callable
from pytamaro import Graphic, Color, transparent, graphic_width
from pytamaro import rectangle, empty_graphic
from pytamaro import beside, above, pin, compose, overlay
from pytamaro import top_center


# error messages
from error_messages import arguments_error_message, CastleType

# helper functions
from color_functions import set_value, get_value

# measurements
from measurements import support_height_cm, support_count, support_width_cm, wall_side_cm, battlement_height_cm
from measurements import merlon_count, merlon_height_cm, merlon_width_cm

### helper functions

def beside_list_gap(l: list[Graphic], gap_width: float) -> Graphic:
    """gaps are placed between graphics, not before nor after"""
    gap = rectangle(gap_width, 0, transparent)
    result = empty_graphic()
    for i in range(len(l) * 2):
        result = beside(
            result, l[i // 2] if i % 2 == 0 else gap if i != len(l) * 2 - 1 else empty_graphic()
        )
    return result


### supports

def support_piece(width: float, height: float, color: Color) -> Graphic:
    dark_color = set_value(color, get_value(color) * 0.85)
    small_height = height * 0.15
    return above(
        rectangle(width, height - small_height, color),
        rectangle(width, small_height, dark_color)
    )


def support(width: float, height: float, lighter_color: Color) -> Graphic:
    piece_count = 3
    result = empty_graphic()
    for i in range(piece_count):
        new_color = set_value(lighter_color, get_value(
            lighter_color) / (1.1 + i * 0.3))
        result = above(
            result,
            support_piece(
                width, height / piece_count,
                new_color)
        )
    return result


def supports(pix_per_cm: float, lighter_color: Color) -> Graphic:
    support_width = support_width_cm * pix_per_cm
    support_height = support_height_cm * pix_per_cm
    gap_width = 2 * support_width
    shade_color = set_value(lighter_color, get_value(lighter_color) * 0.75)
    supports = [support(support_width, support_height,
                        lighter_color)] * support_count
    return compose(
        pin(top_center, beside_list_gap(supports, gap_width)),
        pin(top_center, rectangle(wall_side_cm *
            pix_per_cm, support_height / 3, shade_color))
    )


# the battlement

def battlement(color: Color, merlon_function: Callable[[float, Color], Graphic]) -> Graphic:
    # ensure that the first parameter is a color
    assert isinstance(color, Color), arguments_error_message(battlement, 0, CastleType.COLOR)
    # ensure that the second parameter is a merlon
    assert isinstance(merlon_function, Callable), arguments_error_message(battlement, 1, CastleType.MERLON)

    pix_per_cm = 1
    # measurements
    height = battlement_height_cm * pix_per_cm
    width = wall_side_cm * pix_per_cm
    merlon_height = merlon_height_cm * pix_per_cm
    merlon_width = merlon_width_cm * pix_per_cm
    # components
    merlon = merlon_function(pix_per_cm, color)
    #  return empty_graphic if merlon function is no_merlon
    if graphic_width(merlon) == 0:
        return empty_graphic()
    merlons = [merlon] * merlon_count
    bottom_wall = rectangle(width, height - merlon_height, color)
    bottom_wall = overlay(supports(pix_per_cm, color), bottom_wall)
    return above(
        beside_list_gap(merlons, merlon_width),
        bottom_wall
    )

