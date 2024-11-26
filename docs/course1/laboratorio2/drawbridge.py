from pytamaro import Color, Graphic, hsv_color, black, graphic_height, graphic_width
from functools import reduce
from pytamaro import rectangle, circular_sector, empty_graphic, triangle
from pytamaro import pin, compose, overlay, above, rotate, beside, transparent
from pytamaro import top_right, bottom_left, top_left, bottom_center, top_center, center, bottom_right, center_left


# error messages
from error_messages import arguments_error_message, CastleType


from wall import wall
from wall_properties import ivy, nothing, bricks
from composition import above_list  
from color_functions import set_value, get_value
from color_functions import light_wood_color, dark_wood_color, hole_color
from colors import grey


ivy_wall = wall(grey, True, ivy)
normal_wall = wall(grey, False, nothing)
brick_wall = wall(grey, True, bricks)



# Helper Functions

def beside_list(l: list[Graphic]) -> Graphic:
    result = empty_graphic()
    for g in l:
        result = beside(result, g)
    return result


# THE CHAIN

def link_bar(width: float, height: float, line_thickness: float, color: Color, dark_color: Color) -> Graphic:
    assert width > 2 * line_thickness
    return overlay(
        rectangle(width - 2 * line_thickness, height, color),
        rectangle(width, height, dark_color)
    )


def round_bar(width: float, line_thickness: float, color: Color, dark_color, linked: bool) -> Graphic:
    radius = width / 2
    result = compose(
        pin(bottom_center, circular_sector(radius - line_thickness, 180, color)),
        pin(bottom_center, circular_sector(radius, 180, dark_color))
    )
    if not linked:
        return result
    else:
        side_link_width = width / 3
        side_link = link_bar(side_link_width, radius, line_thickness, color, dark_color)
        return overlay(side_link, result)


def link_center(width: float, height: float, line_thickness: float,
                color: Color, dark_color: Color, linked_up: bool, linked_down: bool) -> Graphic:
    bar_width = width / 3
    side = link_bar(bar_width, height, line_thickness, color, dark_color)
    link_end = round_bar(bar_width, line_thickness, color, dark_color, False)

    central_piece = rectangle(bar_width, height, transparent)
    if linked_up:
        central_piece = compose(
            pin(top_center, rotate(180, link_end)),
            pin(top_center, central_piece)
        )
    if linked_down:
        central_piece = compose(
            pin(bottom_center, link_end),
            pin(bottom_center, central_piece)
        )
    return beside_list([side, central_piece, side])


def link(width: float, height: float, line_thickness: float, color: Color, dark_color: Color, linked_up: bool, linked_down: bool) -> Graphic:
    assert height >= width
    return above(
        round_bar(width, line_thickness, color, dark_color, linked_up),
        above(
            link_center(width, height - width, line_thickness, color, dark_color, linked_up, linked_down),
            rotate(180, round_bar(width, line_thickness, color, dark_color, linked_down))
        )
    )


def chain(width: float, height: float, color: Color) -> Graphic:
    link_height = width / 2 * 3
    side_link_height = link_height - width
    link_count = int((height + side_link_height) // (link_height + side_link_height))

    actual_height = link_count * link_height + (link_count - 1) * side_link_height
    height_difference = height - actual_height
    height_increase = height_difference / (2 * link_count - 1)

    link_height += height_increase
    side_link_height += height_increase
    dark_color = set_value(color, get_value(color) * 0.25)
    line_thickness = width / 15
    # fill the extra space by spacing out front links by the needed amount
    side_link_height = (height - link_count * link_height) / (link_count - 1)
    side_link = link_bar(width / 3, side_link_height, line_thickness, color, dark_color)
    result = empty_graphic()
    for i in range(link_count):
        linked_up = i != 0
        linked_down = i != link_count - 1
        result = above(
            result,
            above(
                link(width, link_height, line_thickness, color, dark_color, linked_up, linked_down),
                side_link if linked_down else empty_graphic()
            )
        )
    return result


# THE ARCH



# CONSTANTS
dark_grey = set_value(grey, get_value(grey) * 0.8)
dark_dark_grey = set_value(dark_grey, get_value(dark_grey) * 0.8)

from measurements import wall_side_cm, pix_per_cm


def arch(color: Color) -> Graphic:
    # colors
    empty_color = hole_color(color)
    frame_color = set_value(color, get_value(color) * 0.8)

    width = pix_per_cm * wall_side_cm * 0.8
    height = pix_per_cm * wall_side_cm
    radius = width / 2
    frame_thickness = width / 7
    hole_width = width - 2 * frame_thickness
    hole_radius = radius - frame_thickness

    background = rectangle(height, height, color)

    top_hole = circular_sector(hole_radius, 180, empty_color)
    bottom_hole = rectangle(hole_width, height - radius, empty_color)
    hole = pin(bottom_center, above(top_hole, bottom_hole))
    frame = above(top_frame(radius, frame_color), bottom_frame(width, height - radius, frame_color))
    frame = pin(bottom_center, frame)
    background = pin(bottom_center, background)

    return compose(hole, compose(frame, background))


def bottom_frame(width: float, height: float, color: Color) -> Graphic:
    dark_color = set_value(color, get_value(color) * 0.6)
    brick_count = 4
    separator_height = height / 20
    brick_height = (height - brick_count * separator_height) / brick_count
    brick = above(
        rectangle(width, brick_height, color),
        rectangle(width, separator_height, dark_color)
    )
    result = empty_graphic()
    for _ in range(brick_count):
        result = above(result, brick)
    return result


def top_frame(radius: float, color: Color) -> Graphic:
    background = circular_sector(radius, 180, color)
    dark_color = set_value(color, get_value(color) * 0.6)
    brick_count = 6
    separator_angle = 5
    rotation_angle = (180 / brick_count)

    separator = circular_sector(radius, separator_angle, dark_color)
    result = background
    for i in range(brick_count):
            result = compose(rotate(i*rotation_angle, separator), result)
    return compose(
        rotate(180 - separator_angle, separator),
        result
    )


# THE DRAWBRIDGE

def compose_beside(graphics: list[Graphic], bottom_pin: bool = False) -> Graphic:
    result = empty_graphic()
    for graphic in graphics:
        result = pin(bottom_right if bottom_pin else top_right, result)
        result = compose(result, pin(bottom_left if bottom_pin else top_left, graphic))
    return pin(center, result)


def borderer(g: Graphic, color: Color, border_thickness: int, top_border: bool = True, right_border: bool = True, bottom_border: bool = True, left_border: bool = True) -> Graphic:
    """Returns a graphic with a border of the given color. The width and height remain the same"""

    if top_border:
        top_border = pin(
            top_left,
            rectangle(graphic_width(g), border_thickness, color)
        )
    if bottom_border:
        bottom_border = pin(
            bottom_left,
            rectangle(graphic_width(g), border_thickness, color)
        )
    if left_border:
        left_border = pin(
            top_left,
            rectangle(border_thickness, graphic_height(g), color)
        )
    if right_border:
        right_border = pin(
            top_right,
            rectangle(border_thickness, graphic_height(g), color)
        )
    
    result = g
    if top_border:
        result = compose(top_border, pin(top_left, result))
    if bottom_border:
        result = compose(bottom_border, pin(bottom_left, result))
    if left_border:
        result = compose(left_border, pin(top_left, result))
    if right_border:
        result = compose(right_border, pin(top_right, result))

    return result


def latch_body(width: float, height: float, color: Color) -> Graphic:
    return rectangle(width, height, color)


def latch_with_point(height: float, color: Color) -> Graphic:
    triangular_body_height = height * 2

    triangular_body = above(
        rotate(90, triangle(height / 2, triangular_body_height, 90, color)),
        rotate(180, triangle(triangular_body_height, height / 2, 90, color))
    )

    triangular_body = pin(center_left, triangular_body)

    heart_square = pin(top_right, rectangle(height, height, color))
    heart_ear = pin(bottom_right, circular_sector(height / 2, 180, color))
    heart = compose(
        heart_square,
        heart_ear
    )

    heart = compose(
        heart,
        pin(top_left, rotate(-90, heart_ear))
    )

    heart = rotate(-45, heart)

    body_with_heart = compose(
        pin(center, heart),
        triangular_body
    )

    return compose(
        circular_sector(height / 4, 360, black),
        body_with_heart
    )


def latch(width: float, height: float, color: Color) -> Graphic:
    return beside(
        latch_with_point(height, color),
        latch_body(width, height, color)
    )


# A bar is one of the branches constituting the rhombus shape in the final Graphic
def bar(bar_width: float, bar_height: float, color: Color) -> Graphic:
    triangle_bar = triangle(bar_height, bar_height, 90, color)
    rectangle_bar = rectangle(bar_width, bar_height, color)
    graphic = compose(pin(top_left, compose(pin(top_left, rotate(-90, triangle_bar)), pin(top_right, rectangle_bar))), pin(top_right, rotate(180, triangle_bar)))
    return graphic


def rhombus(width: float, height: float, color: Color):
    bar_element = bar(width, height / 4, color)
    rhombus_base = compose(
    rotate(90, pin(top_right, bar_element)),
    pin(top_left, bar_element)
    )
    rhombus_final = compose(
    pin(bottom_left, rhombus_base),
    pin(bottom_left, rotate(180, rhombus_base))
    )
    return rhombus_final


def cross(width: float, height: float, color: Color) -> Graphic:
    frame_width = width / 10.0
    shade_1 = above_list(
    [rectangle(width, frame_width * 1.2, hsv_color(1, 0.9, 0.16, 0.9)),
    rectangle(width, frame_width / 4.0, hsv_color(1, 0.9, 0.16,  0.7)),
    rectangle(width, frame_width / 5.0, hsv_color(1, 0.9, 0.16,  0.3))]
    )
    shade_2 = above_list(
    [rectangle(width, frame_width / 5.0, hsv_color(1, 0.9, 0.16, 0.9)),
    rectangle(width, frame_width / 5.0, hsv_color(1, 0.9, 0.16,  0.7)),
    rectangle(width, frame_width / 6.0, hsv_color(1, 0.9, 0.16,  0.3))]
    )

    cross_vertical = compose(
    pin(top_center, rectangle(width / 11.0, height, color)),
    pin(top_center, shade_1)
    )
    cross_horizontal = above(
    rectangle(width, width / 11.0, color),
    shade_2
    )
    cross = overlay(cross_vertical, cross_horizontal)
    return cross


def plank(bridge_width: float, bridge_height: float, color: Color, number_of_planks: int) -> Graphic:
    plank_height = bridge_height / number_of_planks
    plank_width = bridge_width
    plank_width_outline = plank_width - (plank_height / 15.0)
    plank_height_outline = plank_height - (plank_height / 15.0)
    plank = overlay(rectangle(plank_width_outline, plank_height_outline, color), rectangle(plank_width, plank_height, black))
    return plank


def closed_drawbridge(width: float, height: float, color_background: Color, color_foreground: Color, number_of_planks: float) -> Graphic:
    metal_color = hsv_color(27, 0.48, 0.3)
    
    frame_width = width / 10.0
    plank_element = plank(width, height, color_background, number_of_planks)
    background_bridge = reduce(above, [plank_element] * number_of_planks, empty_graphic())
    with_cross = overlay(cross(width, height, color_foreground), background_bridge)
    latch_element = latch(width / 30.0, width / 30.0, metal_color)
    bridge_base = overlay(rotate(45, rhombus(width / 4, height / 4, color_foreground)), with_cross)
    bridge_framed = borderer(bridge_base, color_foreground, frame_width)
    bridge_final = compose(
    pin(top_center, rotate(90, latch_element)),
    pin(top_center, compose(pin(bottom_center, rotate(-90, latch_element)), pin(bottom_center, bridge_framed)))
    )
    return bridge_final


def drawbridge(open: bool) -> Graphic:
    # ensure that the first parameter is a drawbridge state
    assert isinstance(open, bool), arguments_error_message(drawbridge, 0, CastleType.DRAWBRIDGE_STATE)

    light_color = light_wood_color(grey)
    dark_color = dark_wood_color(grey)
    plank_count = 8
    
    height = pix_per_cm * wall_side_cm * 0.9
    width = height * 0.8

    bridge_thickness = height / 15
    arch_bridge = arch(grey)
    if not open:
        d = compose(
            pin(bottom_center, closed_drawbridge(width, height, dark_color, light_color, plank_count)),
            pin(bottom_center, arch_bridge)
        ) 
    else:
        chain_width = width / 15
        beam = rectangle(chain_width * 1.5, chain_width * 1.7, light_color)
        my_chain = compose(
            pin(top_center, beam),
            pin(top_center, chain(chain_width, height - bridge_thickness, hsv_color(0, 0, 0.3)))
            )
        
        open_bridge_from_front = rectangle(width, bridge_thickness, light_color)
        intermediate = compose(
            pin(top_right, my_chain),
            pin(top_right, compose(
                pin(bottom_left, my_chain),
                pin(top_left, open_bridge_from_front)
            ))
        )
        d = compose(
            pin(bottom_center, intermediate),
            pin(bottom_center, arch_bridge)
        )

    return d
        

