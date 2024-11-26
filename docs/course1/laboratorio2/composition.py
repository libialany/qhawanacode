from pytamaro import (
    Graphic,
    empty_graphic,
    above, compose, pin, overlay,
    bottom_left, bottom_right
)

# error messages
from error_messages import arguments_error_message, CastleType


def above_list(l: list[Graphic]) -> Graphic:
    # ensure that the first parameter is list of castle pieces
    assert isinstance(l, list), arguments_error_message(above_list, 0, CastleType.LIST)

    result = empty_graphic()
    for g in l:
        result = above(result, g)
    return result


def beside_list(l: list[Graphic]) -> Graphic:
    """this actually composes by alligning on the bottom!"""
    # ensure that the first parameter is list of castle pieces
    assert isinstance(l, list), arguments_error_message(beside_list, 0, CastleType.LIST)

    result = empty_graphic()
    for g in l:
        result = compose(
            pin(bottom_right, result),
            pin(bottom_left, g)
        )
    return result


def overlay_list(l: list[Graphic]) -> Graphic:
    result = empty_graphic()
    for g in l:
        result = overlay(result, g)
    return result