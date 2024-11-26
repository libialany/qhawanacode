from pytamaro import Graphic, Color
from pytamaro import circular_sector, rectangle
from pytamaro import rotate, beside, above

# constants
from measurements import merlon_width_cm, merlon_height_cm


# helper functions

def round_part(width: float, color: Color, concave: bool) -> Graphic:
    radius = width / 2
    quarter = circular_sector(radius, 90, color)
    if concave:
        return beside(quarter, rotate(90, quarter))
    else:
        return beside(rotate(90, quarter), quarter)
    

def rounded_merlon_generic(pix_per_cm: float, color: Color, concave: bool = True) -> Graphic:
    width = merlon_width_cm * pix_per_cm
    height = merlon_height_cm * pix_per_cm

    bottom_part_height = height - width / 2
    bottom_part = rectangle(width, bottom_part_height, color)
    return above(round_part(width, color, concave), bottom_part)



# the merlons

# split merlon
def split_merlon(pix_per_cm: float, color: Color) -> Graphic:
    return rounded_merlon_generic(pix_per_cm, color, True)


# rounded merlon
def rounded_merlon(pix_per_cm: float, color: Color) -> Graphic:
    return rounded_merlon_generic(pix_per_cm, color, False)


# rectangular merlon
def rectangular_merlon(pix_per_cm: float, color: Color) -> Graphic:
    width = merlon_width_cm * pix_per_cm
    height = merlon_height_cm * pix_per_cm
    return rectangle(width, height, color)