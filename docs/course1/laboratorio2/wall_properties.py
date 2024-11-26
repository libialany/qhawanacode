from typing import Callable
from math import atan, degrees, sin, pi
from pytamaro import Graphic, Color, Point, black, hsv_color, graphic_width, transparent, white
from pytamaro import triangle, rectangle, empty_graphic, circular_sector, graphic_height
from pytamaro import compose, rotate, pin, beside, above, overlay, ellipse
from pytamaro import bottom_right, top_left, top_right, bottom_left, bottom_center, center_left, center, center_right

# helper functions
from color_functions import get_value, set_value, set_hue, get_saturation, set_saturation
from color_functions import dark_leaf_color, light_leaf_color, hole_color
from color_functions import light_wood_color, dark_wood_color
from composition import above_list, overlay_list

# constants
from measurements import door_height_cm, door_width_cm, window_height_cm, pix_per_cm


# helper functions

def beside_list(l: list[Graphic]) -> Graphic:
    result = empty_graphic()
    for g in l:
        result = beside(result, g)
    return result


### helpers - double door

# lockset
def plain_bar(width: float, thickness: float, color: Color) -> Graphic:
    """ bar without knobs """
    horizontal_bar = rectangle(width, thickness, color)
    # bend and vertical bar
    vertical_bar = above(
        circular_sector(thickness, 90, color),
        above(
            rectangle(thickness, width / 6, color),
            rotate(180, circular_sector(thickness / 2, 180, color))
        )
    )
    # compose horizontal bar with the vertical bar
    return compose(
        pin(top_right, horizontal_bar),
        pin(top_left, vertical_bar)
    )


def bar(width: float, thickness: float, color: Color) -> Graphic:
    """ bar with knobs """
    # the knobs have to be split into top part and bottom part
    # to later be pinned in top left of the bar
    knob_offset = thickness / 6  # height that sticks out of bar
    knob_width = width / 10
    top_knob = rectangle(knob_width, knob_offset, color)
    bottom_knob = rectangle(knob_width, thickness + knob_offset, color)
    h_gap = rectangle(knob_width * 2, 0, transparent)
    # initialize knob strips
    top_knobs = top_knob
    bottom_knobs = bottom_knob
    # fill knob strips
    for i in range(2):
        top_knobs = beside(top_knobs, beside(h_gap, top_knob))
        bottom_knobs = beside(bottom_knobs, beside(h_gap, bottom_knob))
    top_knobs = pin(bottom_left, top_knobs)
    bottom_knobs = pin(top_left, bottom_knobs)
    # compose knobs and bar
    return compose(
        top_knobs,
        compose(
            bottom_knobs,
            pin(top_left, plain_bar(width, thickness, color))
        )
    )


def lock(width: float, height: float, color: Color) -> Graphic:
    """ multiple bars one above the other """
    bar_count = 3
    gap_height = height / (bar_count * 2 + 1)
    bar_thickness = gap_height / 5
    one_bar = bar(width, bar_thickness, color)
    v_gap = rectangle(0, gap_height, transparent)
    result = one_bar
    for i in range(bar_count - 1):
        result = above(result, above(v_gap, one_bar))
    return result


def right_trapezoid(width: float, height: float, color: Color, is_left: bool) -> Graphic:
    """ triangle on top of rectangle, or just triangle if height is smaller than width"""
    triangle_side = width if height > width else height
    tri = rotate(90 if is_left else 0, triangle(
        triangle_side, triangle_side, 90, color))
    return tri if height <= width else above(tri, rectangle(width, height - triangle_side, color))


def door_shape(width: float, height: float, color: Color, is_left: bool) -> Graphic:
    """ circular sector on top of rectangle """
    return above(
        rotate(90 if is_left else 0, circular_sector(width, 90, color)),
        rectangle(width, height - width, color)
    )


def compose_list_point(point: Point, list: list[Graphic]) -> Graphic:
    """ composes given list pinned in given point, first element goes on background """
    result = empty_graphic()
    for element in list:
        result = compose(
            pin(point, element),
            pin(point, result)
        )
    return result


# multiple trapezoids
def stripes(width: float, height: float, color: Color, dark_color: Color, is_left: bool, count: int) -> Graphic:
    # constants
    gap_height = height / count
    thickness = gap_height / 8
    # composition
    graphics = []
    for i in range(count):
        new_height = height - i * gap_height
        graphics.append(
            right_trapezoid(
                width, new_height, dark_color, is_left)
        )
        graphics.append(
            right_trapezoid(
                width, new_height - thickness, color, is_left)
        )
    return compose_list_point(bottom_right if is_left else bottom_left, graphics)


def bolt(size: float, color: Color) -> Graphic:
    return ellipse(size, size, color)


def bolts(width: float, height: float, color: Color, board_count: int, is_left: bool) -> Graphic:
    """ half transparent pattern of bolts to be overlayed on a half door """
    # constants
    bolt_size = height / 50
    v_gap_size = (height - board_count * bolt_size) / board_count
    v_gap = rectangle(0, v_gap_size, transparent)
    # must follow ratio 1:1 to follow inclination of stripes
    h_gap_size = v_gap_size
    h_gap = rectangle(h_gap_size, 0, transparent)
    col_count = (width - board_count * bolt_size) // h_gap_size
    # composition
    result = empty_graphic()
    for i in range(int(col_count) + 1):
        col = empty_graphic()
        for j in range(board_count + 1 - i):
            # no gap before first bolt
            # first two columns have same number of bolts
            new_bolt = above(
                v_gap if j != 0 else empty_graphic(),
                bolt(bolt_size, color) if i != 0 or j != 0 else empty_graphic()
            )
            col = above(
                col,
                new_bolt
            )
        if is_left:
            # no gap after rightmost column
            result = compose(
                pin(bottom_right,
                    beside(
                        col,
                        h_gap if i != 0 else empty_graphic(),
                    )
                    ),
                pin(bottom_left, result)
            )
        else:
            # no gap before lefmost column
            result = compose(
                pin(bottom_right, result),
                pin(bottom_left,
                    beside(
                        h_gap if i != 0 else empty_graphic(),
                        col
                    )
                    )
            )
    return result


def half_door(width: float, height: float, color: Color, dark_color: Color, is_left: bool) -> Graphic:
    # constants
    thickness = height / 100
    board_count = 7
    # composition
    result = compose_list_point(
        bottom_right if is_left else bottom_left,
        [
            door_shape(width, height, dark_color, is_left),
            door_shape(width - thickness, height - thickness, color, is_left),
            stripes(width, height, color, dark_color, is_left, board_count)
        ]
    )
    return compose_list_point(
        bottom_center,
        [result, bolts(width, height, dark_color, board_count, is_left)]
    )


def unlocked_double_door(pix_per_cm: float, wall_color: Color, open: bool) -> Graphic:
    # colors
    light_color = light_wood_color(wall_color)
    dark_color = dark_wood_color(wall_color)
    shadow_color = hsv_color(0, 0, 0.15)
    # dimensions
    height = door_height_cm * pix_per_cm
    width = door_width_cm * pix_per_cm
    # components
    chink = rectangle(width / 100, height, dark_color)
    open_door_side = rectangle(width / 15, height - width / 2, light_color)
    open_left_door = compose(
        pin(bottom_left, open_door_side),
        pin(bottom_left, door_shape(width / 2, height, shadow_color, True))
    )

    beside_doors = beside(
        open_left_door if open else half_door(width / 2, height, light_color, dark_color, True),
        half_door(width / 2, height, light_color, dark_color, False)
    )
    # add chink to door
    result = compose_list_point(bottom_center, [beside_doors, chink])
    # add lockset to door
    return compose(
        pin(center_left, lock(width / 3, height, dark_color)),
        pin(center, result)
    )


## helpers - door

def door_stripe(width: float, height: float, color: Color) -> Graphic:
    return rectangle(width, height, color)


def door_back(width: float, height: float, stripes_number: int, color: Color) -> Graphic:
    separator_width = 2
    separator = rectangle(separator_width, height,
                          set_value(color, get_value(color) * 0.5))
    separator_number = stripes_number - 1

    return beside_list(
        [
            compose(
                pin(center_right, separator) if i != separator_number else empty_graphic(),
                pin(center_right, door_stripe(
                    width // stripes_number, height, color))
            ) for i in range(separator_number + 1)
        ]
    )


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

    return compose(
        pin(center, heart),
        triangular_body
    )


def latch(width: float, height: float, color: Color) -> Graphic:
    return beside(
        latch_with_point(height, color),
        latch_body(width, height, color)
    )


def all_latches(width: float, height: float, stripes_number: int, color: Color) -> Graphic:
    latch_width = (width / stripes_number) * (stripes_number - 2)
    gap_height = height / 4
    latch_height = width / 9
    latch_piece = latch(latch_width, latch_height, color)

    return above_list(
        [
            latch_piece,
            rectangle(latch_width, gap_height, transparent),
            latch_piece,
            rectangle(latch_width, gap_height, transparent),
            latch_piece
        ]
    )


## helpers - rounded window

def ring_sector_list(diameter: float, start_angle: float, end_angle: float, pieces: list[Graphic]) -> Graphic:
    result = empty_graphic()
    angle_delta = (end_angle - start_angle) / len(pieces)
    angle = start_angle
    for piece in pieces:
        spacer = rectangle(diameter / 2, 0, black)
        offset_piece = pin(center_left, beside(spacer, piece))
        result = compose(result, rotate(angle, offset_piece))
        angle += angle_delta
    return result


def ring_list(diameter: float, pieces: list[Graphic]) -> Graphic:
    return ring_sector_list(diameter, 0, 360, pieces)


def ring_sector(diameter: float, start_angle: float, end_angle: float, piece: Graphic, count: int) -> Graphic:
    return ring_sector_list(diameter, start_angle, end_angle, [piece] * count)


def arch(radius: float, brick_width: float, brick_count: int, brick_color: Color) -> Graphic:
    # dimensions
    inner_radius = radius - brick_width
    arch_perimeter =  inner_radius * pi
    brick_height = 0.8 * arch_perimeter / brick_count
    # components
    brick = rectangle(brick_width, brick_height, brick_color)
    return ring_sector(2 * radius , 45, 150 , brick, brick_count)


def brick_round(width: float, height: float, color: Color, crease_color: Color, has_spacing: bool) -> Graphic:
    if not has_spacing:
        return rectangle(width, height, color)
    else:
        horizontal_spacing_width = width / 9
        return beside(
            rectangle(width - horizontal_spacing_width, height, color),
            rectangle(horizontal_spacing_width, height, crease_color)
        )


def brick_column(height: float, brick_width: float, brick_count: int, brick_color: Color, crease_color: Color, has_spacing: bool) -> Graphic:
    # dimensions
    brick_presence = 0.75  # ratio of presence of bricks in column
    brick_height = height * brick_presence / brick_count
    gap_height = height * (1 - brick_presence) / brick_count
    # components
    my_brick = brick_round(brick_width, brick_height, brick_color, crease_color, has_spacing)
    gap = rectangle(brick_width, gap_height, crease_color)
    return above_list([
        my_brick if (i + 1) % 4 == 0 else rotate(180, my_brick) if (i + 1) % 2 == 0 else gap for i in range(brick_count * 2)
    ])


### helpers - window

def window_right_trapezoid(bottom_width: float, height: float, top_width: float, color: Color, flip: bool) -> Graphic:
    assert top_width <= bottom_width
    assert height > 0
    assert bottom_width > 0
    w_diff = bottom_width - top_width
    tri = rotate(-90 if flip else 0, triangle(w_diff if not flip else height,
                 height if not flip else w_diff, 90, color))
    rec = rectangle(bottom_width - w_diff, height, color)
    return beside(rec, tri)


def trapezoid_brick(width: float, height: float, outline_thick: float, color: Color, outline_color: Color, flip: bool) -> Graphic:
    trap_diff = outline_thick + (0.5 * outline_thick / sin(pi / 4))
    small_trap_width = width - trap_diff - outline_thick / 2
    small_trap_height =  height - 2 * outline_thick
    trapezoids = compose(
        pin(
            center_left,
            window_right_trapezoid(small_trap_width, small_trap_height, small_trap_width - small_trap_height, color, flip)
        ),
        pin(
            center_left,
            window_right_trapezoid(width - outline_thick / 2, height, width - height, outline_color, flip)
        )
    )
    return beside(rectangle(outline_thick / 2, height, outline_color), trapezoids)


def brick(width: float, height: float, outline_thick: float, color: Color, outline_color: Color) -> Graphic:
    return overlay(
        rectangle(width - outline_thick, height - 2 * outline_thick, color),
        rectangle(width, height, outline_color)
    )


def frame_side(width: float, height: float, outline_thick: float, brick_count: int, color: Color) -> Graphic:
    assert brick_count >= 2
    brick_width = width / brick_count
    # colors
    outline_color = set_value(color, get_value(color) * 0.75)

    left_corner = rotate(180, trapezoid_brick(brick_width, height, outline_thick, color, outline_color, True))
    right_corner = trapezoid_brick(brick_width, height, outline_thick, color, outline_color, False)
    center_part = beside_list([
        brick(brick_width, height, outline_thick, color, outline_color) for i in range(brick_count - 2)
        ]
    )
    return rotate(180, beside(beside(left_corner, center_part), right_corner))


def frame(width: float, height: float, frame_thick: float, h_count: int, v_count: int, color: Color) -> Graphic:
    outline_thick = frame_thick / 10  # adjustable
    top_side = frame_side(width, frame_thick, outline_thick, h_count, color)
    left_side = rotate(90, frame_side(height, frame_thick, outline_thick, v_count, color))
    # combine left side and top side
    result = compose(
        pin(top_left, top_side),
        pin(top_left, left_side)
    )
    # attach right side
    result = compose(
        pin(top_right, result),
        pin(top_right, (rotate(180, left_side)))
    )
    # attach bottom_side
    return compose(
        pin(bottom_right, result),
        pin(bottom_right, rotate(180, top_side))
    )



### the doors

### double door

def double_door(wall_side: float, wall_color: Color) -> Graphic:
    result = unlocked_double_door(pix_per_cm, wall_color, False)
    # transparent background for texture
    transparent_background = rectangle(wall_side, wall_side, transparent)
    return compose(
        pin(bottom_center, result), 
        pin(bottom_center, transparent_background))


### door

def door(wall_side: float, wall_color: Color) -> Graphic:
    # colors
    light_color = light_wood_color(wall_color)
    dark_color = dark_wood_color(wall_color)
    stripes_number = 5
    # measurements
    door_height = door_height_cm * pix_per_cm
    door_width = door_width_cm * pix_per_cm
    result = compose(
        pin(center_right, all_latches(door_width, door_height * 0.9, stripes_number, dark_color)),
        pin(center_right, door_back(door_width, door_height, stripes_number, light_color))
    )
    # transparent background for texture
    transparent_background = rectangle(wall_side, wall_side, transparent)
    return compose(
        pin(bottom_center, result), 
        pin(bottom_center, transparent_background))


### the windows

### window

def window(wall_side: float, wall_color: Color) -> Graphic:
    # constants
    h_brick_count = 2
    v_brick_count = 3
    window_height = window_height_cm * pix_per_cm
    window_width = 2 / 3 * window_height

    frame_thick = window_width / 5
    frame_color = set_value(wall_color, get_value(wall_color) * 0.8)
    content_color = hole_color(wall_color)
    result = overlay(
        frame(window_width, window_height, frame_thick, h_brick_count, v_brick_count, frame_color),
        rectangle(window_width, window_height, content_color)
    )

    # transparent background for texture
    transparent_background = rectangle(wall_side, wall_side, transparent)
    return overlay(result, transparent_background)


### rounded window

def arched_window(wall_side: float, wall_color: Color) -> Graphic:
    # constants
    col_brick_count = 7
    arch_brick_count = 7
    has_spacing = True
    # colors
    brick_color = set_value(wall_color, get_value(wall_color) * 0.75)
    window_color = hole_color(wall_color)
    crease_color = set_saturation(set_value(wall_color, get_value(wall_color) * 1.5), get_saturation(wall_color) * 0.65)
    wood_color = set_value(wall_color, get_value(wall_color) * 0.7)
    # dimensions
    window_height = window_height_cm * pix_per_cm
    window_width = window_height / 5 * 4
    brick_width = window_width / 4
    brick_column_height = window_height / 3 * 2
    wood_piece_height = window_height / 20
    # components
    wood_piece = rectangle(window_width, wood_piece_height, wood_color)
    window = rectangle(window_width - 2 * brick_width, brick_column_height, window_color)
    column = brick_column(brick_column_height, brick_width, col_brick_count, brick_color, crease_color, has_spacing)
    bottom_part = beside(
        column, beside(window, rotate(180, column))
    )
    result = compose(
        arch(window_height / 2 * 1.1, brick_width * 1.15, arch_brick_count, brick_color),
        above(wood_piece, bottom_part)
    )

    # transparent background for texture
    transparent_background = rectangle(wall_side, wall_side, transparent)
    return overlay(result, transparent_background)


# old version of name - kept in order to avoid errors if someone has an older version
def rounded_window(wall_side: float, wall_color: Color) -> Graphic:
    return arched_window(wall_side, wall_color)


### textures

### nothing

def nothing(wall_side: float, color: Color) -> Graphic:
    return rectangle(wall_side, wall_side, transparent)


### bricks

def texture_brick(width: float, height: float, color: Color) -> Graphic:
    # colors
    dark_color = set_value(color, get_value(color) * 0.65)
    # measurements
    outline_thickness = height / 8
    rec_height = (height - 3 * outline_thickness) / 2
    recs_width = width - 3 * outline_thickness  # small and big together
    small_rec_width = recs_width / 4
    big_rec_width = recs_width - small_rec_width
    # components
    small_rec = rectangle(small_rec_width, rec_height, color)
    big_rec = rectangle(big_rec_width, rec_height, color)
    h_gap = rectangle(outline_thickness, rec_height, dark_color)
    v_gap = rectangle(width, outline_thickness, dark_color)
    first_row = beside_list(
        [h_gap, small_rec, h_gap, big_rec, h_gap]
    )
    return above_list(
        [v_gap, first_row, v_gap, rotate(180, first_row), v_gap]
    )


def bricks(wall_side: float, color: Color) -> Graphic:
    brick_width = wall_side / 4.5
    brick_height = brick_width / 2
    brick_color = set_value(color, get_value(color) * 0.9)
    x_coordinates = [wall_side / 4, wall_side * 5 / 7, wall_side * 4 / 9] 
    y_coordinates = [wall_side / 5, wall_side * 1 / 2, wall_side * 5 / 6]

    result = rectangle(wall_side, wall_side, transparent)
    for i in range(len(x_coordinates)):
        gap = rectangle(
            x_coordinates[i], y_coordinates[i], transparent)
        new_piece = compose(
            texture_brick(brick_width, brick_height, brick_color),
            pin(top_right, gap)
        )
        result = compose(
            pin(bottom_left, new_piece), 
            pin(bottom_left, result)
        )
    return result

### ivy

def heart(size: float, color: Color) -> Graphic:
    heart_square = pin(top_right, rectangle(size, size, color))
    heart_round = pin(bottom_right, circular_sector(size / 2, 180, color))
    heart = compose(
        heart_square,
        heart_round
    )
    return rotate(45, compose(
        pin(bottom_left, rotate(-90, heart_round)),
        pin(bottom_right, heart)
    ))


def leaf(size: float, wall_color: Color) -> Graphic:
    outline_thickness = size / 5
    light_color = light_leaf_color(wall_color)
    dark_color = dark_leaf_color(wall_color)
    return overlay(
        heart(size - 2 * outline_thickness, light_color),
        heart(size, dark_color)
    )


def rounded_ivy_f(x: float) -> float:
    return (x / 2 - 2) ** 2 + 1


def rounded_ivy_f_dx(x: float) -> float:
    return x / 2 - 2


def straight_ivy_f(x: float) -> float:
    return x * 1 / 3


def straight_ivy_f_dx(x: float) -> float:
    return 1 / 3


def slope_to_angle(slope: float) -> Graphic:
    return degrees(atan(slope))


def oriented_plotter(f: Callable[[float], float], f_dx: Callable[[float], float], x_min: float, x_max: float, n: int, scale: float, item: Graphic,  debugging: bool = False) -> Graphic:
    assert x_min >= 0 and x_max >= x_min
    x_step = (x_max - x_min) / n
    x_coordinates = [x_min + i * x_step for i in range(0, n)]
    y_coordinates = [f(x) for x in x_coordinates]

    result = rectangle(max(x_coordinates) * scale, max(y_coordinates) * scale, white if debugging else transparent)
    for i in range(len(x_coordinates)):
        gap = rectangle(x_coordinates[i] * scale, y_coordinates[i] * scale, transparent)
        new_point = compose(
            rotate(slope_to_angle(f_dx(x_coordinates[i])), item), 
            pin(top_right, gap)
        )
        result = compose(
            pin(bottom_left, new_point),
            pin(bottom_left, result)
        )
    return result


def ivy(wall_side: float, wall_color: Color) -> Graphic:
    leaf_count = 10
    leaf_size = wall_side / (2 * leaf_count)
    scale = 2 * (wall_side - leaf_size * leaf_count) / leaf_count
    my_leaf = leaf(leaf_size, wall_color)
    rounded_ivy = oriented_plotter(
            rounded_ivy_f, rounded_ivy_f_dx, 0, 9, leaf_count, scale, rotate(90, my_leaf))
    straight_ivy = oriented_plotter(
            straight_ivy_f, straight_ivy_f_dx, 0, 6, leaf_count // 2, scale, rotate(-90, my_leaf))
    result = compose(
        pin(center_left, rotate(45, rounded_ivy)),
        pin(center_left, rectangle(wall_side, wall_side, transparent))
    )
    return compose(
        pin(bottom_right, straight_ivy),
        pin(bottom_right, result)
    )


# crack texture

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


def crack(wall_side: float, wall_color: Color) -> Graphic:
    canvas = rectangle(
        wall_side,
        wall_side,
        transparent
    )

    brick_width = 0.2 * wall_side
    brick_height = 0.1 * wall_side
    crack_color = hole_color(wall_color)

    crack_brick = rectangle(
        brick_width,
        brick_height,
        transparent
    )
    bottom_crack_brick = borderer(
        crack_brick, crack_color, 0.01 * wall_side, False, False, True, False)
    right_bottom_crack_brick = borderer(
        crack_brick, crack_color, 0.01 * wall_side, False, True, True, False)

    crack = compose(
        pin(bottom_left, bottom_crack_brick),
        pin(top_right, right_bottom_crack_brick)
    )

    crack = compose(
        pin(bottom_left, crack),
        pin(top_right, right_bottom_crack_brick)
    )

    crack = compose(
        pin(bottom_left, crack),
        pin(bottom_right, bottom_crack_brick)
    )

    crack = compose(
        pin(bottom_left, crack),
        pin(top_right, right_bottom_crack_brick)
    )

    crack = overlay(
        crack,
        rotate(90, crack)
    )

    return overlay_list([
        crack,
        canvas
    ])