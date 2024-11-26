from pytamaro import (
    Color, rectangle, empty_graphic, beside, above,
    hsv_color, compose, pin, bottom_right, Graphic
)

# error messages
from error_messages import arguments_error_message, CastleType

# helper functions
from color_functions import set_value, get_value

# measurements
from measurements import roof_width, roof_height



# helper functions

def beside_list(l: list[Graphic]) -> Graphic:
    result = empty_graphic()
    for g in l:
        result = beside(result, g)
    return result

# Roof

def new_brick(width: float, height: float, line_thickness: float, color: Color, dark_color: Color):
    brick_foreground = rectangle(width - line_thickness, height - line_thickness, color)
    brick_background = rectangle(width, height, dark_color)
    brick = compose(
        pin(bottom_right, brick_foreground), 
        pin(bottom_right, brick_background))
    return brick


def row(width: float, height: float, line_thickness: float, color: Color, dark_color: Color, brick_count: int) -> Graphic:
    brick = new_brick((width - line_thickness) / brick_count, height, line_thickness, color, dark_color)
    last_border = rectangle(line_thickness, height, dark_color)
    result = empty_graphic()
    for _ in range(brick_count):
        result = beside(result, brick)
    result = beside(result, last_border)
    return result


def new_roof(width: float, height: float, n_bricks: int, n_rows: int, color: Color):
    assert n_bricks >= n_rows
    line_thickness = width / n_bricks * 0.09
    brick_height = (height  - line_thickness) / n_rows
    brick_width = (width - line_thickness) / n_bricks
    color_line = set_value(color, get_value(color) * 0.6)
    brick = new_brick(brick_width, brick_height, line_thickness, color, color_line)
    bottom_line = rectangle(width, line_thickness, color_line)
    side_line = rectangle(line_thickness, brick_height, color_line)
    roof = empty_graphic()
    for i in range(n_rows):
        row = beside_list([brick] * (n_bricks - i))
        row = beside(row, side_line)
        roof = above(row, roof)
    return above(roof, bottom_line)


# generates a rood function in the specified language 
# (this is needed for custom error messages)
def roof(color: Color) -> Graphic:
    # ensure that the first parameter is a color
    assert isinstance(color, Color), arguments_error_message(roof, 0, CastleType.COLOR)

    return new_roof(roof_width, roof_height, 9, 9, color)
