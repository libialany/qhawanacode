from pytamaro import Graphic, Color, Point
from pytamaro import rectangle, empty_graphic
from pytamaro import pin, compose, graphic_height
from pytamaro import bottom_left, bottom_right, top_left, top_right, center_left, center_right

# helper functions
from color_functions import get_value, set_value


### helper functions

def compose_list_point(point: Point, list: list[Graphic]) -> Graphic:
    """ composes given list pinned in given point, first element goes on background """
    result = empty_graphic()
    for element in list:
        result = compose(
            pin(point, element),
            pin(point, result)
        )
    return result


### the brick border

# returns a brick with a shadow underneath and on the side,
# depending if it goes on the left or right border of the wall
def brick(width: float, height: float, color: Color, left: bool) -> Graphic:
    dark_color = set_value(color, get_value(color) * 0.7)
    outline_thickness = height / 7
    result = compose_list_point(
        top_left if left else top_right, [
            rectangle(width, height, dark_color),
            rectangle(width - outline_thickness,
                      height - outline_thickness, color)
        ])
    return result


# creates a border of the given height, with bricks of the given height,
# which goes on the left if `left` is True, otherwise it is mirrored to go on the right
def brick_border(height: float, brick_height: float, color: Color, left: bool) -> Graphic:
    # constants
    brick_count = int(height // brick_height)
    wide_brick_width = brick_height * 1.8
    narrow_brick_width = wide_brick_width * 0.7
    # components
    wide_brick = brick(wide_brick_width, brick_height, color, left)
    narrow_brick = brick(narrow_brick_width, brick_height, color, left)
    result = empty_graphic()
    for i in range(brick_count):
        result = compose(
            pin(bottom_left if left else bottom_right, result),
            pin(top_left if left else top_right, narrow_brick if i %
                2 == 0 else wide_brick)
        )
    return compose(
        pin(center_left if left else center_right, result),
        pin(center_left if left else center_right,
            rectangle(narrow_brick_width, height, color))
    )


# adds brick borders on the sides of the given graphics, as specified by boolean parameters
# `left_border` and `right_border`
def add_brick_borders(graphic: Graphic, brick_height: float, color: Color, left_border: bool, right_border: bool) -> Graphic:
    result = graphic
    if left_border:
        result = compose_list_point(
            center_left, [
                result,
                brick_border(graphic_height(graphic), brick_height, color, True)]
        )
    if right_border:
        result = compose_list_point(
            center_right, [
                result,
                brick_border(graphic_height(graphic), brick_height, color, False)]
        )
    return result