from pytamaro import Color, hsv_color

# RGB to HSV

def min_max_rgb(color: Color) -> tuple[float, float]:
    components = [color.red / 255, color.green / 255, color.blue / 255]
    return min(components), max(components)

def to_hsv(color: Color) -> tuple[float, float, float]:
    min_value, max_value = min_max_rgb(color)
    if min_value == max_value:
        return 0, 0, max_value
    else:
        s = (max_value - min_value) / max_value
        r = color.red / 255
        g = color.green / 255
        b = color.blue / 255
        if max_value == r:
            h = 60 * ((g - b) / (max_value - min_value))
        elif max_value == g:
            h = 60 * (2 + (b - r) / (max_value - min_value))
        else:
            h = 60 * (4 + (r - g) / (max_value - min_value))
        if h < 0:
            h += 360
        return h, s, max_value

def get_hue(color: Color) -> float:
    return to_hsv(color)[0]

def get_saturation(color: Color) -> float:
    return to_hsv(color)[1]

def get_value(color: Color) -> float:
    return to_hsv(color)[2]

def get_opacity(color: Color) -> float:
    return color.alpha


# Manipulation on HSV

def set_value(color: Color, value: float) -> Color:
    h, s, v = to_hsv(color)
    v = value
    # Cap value in range [0-1]
    if v < 0:
        v = 0
    elif v > 1:
        v = 1
    return hsv_color(h, s, v, get_opacity(color))


def set_hue(color: Color, hue: int) -> Color:
    h, s, v = to_hsv(color)
    h = hue
    # Cap hue in range [0-359]
    if h < 0:
        h = 0
    elif h > 359:
        h = 359
    return hsv_color(h, s, v, get_opacity(color))


def set_saturation(color: Color, saturation: int) -> Color:
    h, s, v = to_hsv(color)
    s = saturation
    # Cap saturation in range [0-1]
    if s < 0:
        s = 0
    elif s > 1:
        s = 1
    return hsv_color(h, s, v, get_opacity(color))


### generate property colors based on wall color

def light_leaf_color(wall_color: Color) -> Color:
    h = 130
    s = 0.6
    v = 0.5
    if get_saturation(wall_color) == 0 and get_value(wall_color) < 0.3:
        # if wall is black make it darker
        v = 0.35
    return hsv_color(h, s, v)


def dark_leaf_color(wall_color: Color) -> Color:
    light_color = light_leaf_color(wall_color)
    return set_value(light_color, get_value(light_color) * 0.75)


# inside of windows, open doors, ...
def hole_color(wall_color: Color) -> Color:
    if get_saturation(wall_color) == 0 and get_value(wall_color) < 0.3:
        # if wall is black make it darker
        return hsv_color(0, 0, 0.07)
    return hsv_color(0, 0, 0.1)


def light_wood_color(wall_color: Color) -> Color:
    h = 30
    s = 0.7
    v = 0.6
    if get_saturation(wall_color) == 0 and get_value(wall_color) < 0.3:
        # if wall is black make it darker
        v = 0.5
    return hsv_color(h, s, v)

def dark_wood_color(wall_color: Color) -> Color:
    light_color = light_wood_color(wall_color)
    return set_value(light_color, get_value(light_color) * 0.7)
    