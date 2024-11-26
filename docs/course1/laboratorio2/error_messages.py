# to get the function name dinamically
from enum import Enum


# this file contains functions that generate custom error messages to use in assertions


#  defining possible types for parameters
class CastleType(Enum):
    COLOR = 0
    MERLON = 1
    LIST = 2
    DRAWBRIDGE_STATE = 3
    WALL_BORDER = 4
    WALL_PROPERTY = 5

class Language(Enum):
    ENGLISH = 0
    ITALIAN = 1
    GERMAN = 2


##### mapping types to names in any language

def get_name(castle_type: CastleType, language: Language) -> str:
    if language == Language.GERMAN:
        # to translate in german
        names = {
            CastleType.COLOR: "color",
            CastleType.MERLON: "merlon",
            CastleType.LIST : "list of castle pieces",
            CastleType.DRAWBRIDGE_STATE: "drawbridge state",
            CastleType.WALL_BORDER: "wall border",
            CastleType.WALL_PROPERTY: "wall property"
        }
    elif language == Language.ITALIAN:
        names = {
            CastleType.COLOR: "colore",
            CastleType.MERLON: "merlo",
            CastleType.LIST : "lista di pezzi di castello",
            CastleType.DRAWBRIDGE_STATE: "stato del ponte levatoio",
            CastleType.WALL_BORDER: "bordo per muro",
            CastleType.WALL_PROPERTY: "proprietà muro"
        }
    else:
        names = {
            CastleType.COLOR: "color",
            CastleType.MERLON: "merlon",
            CastleType.LIST : "list of castle pieces",
            CastleType.DRAWBRIDGE_STATE: "drawbridge state",
            CastleType.WALL_BORDER: "wall border",
            CastleType.WALL_PROPERTY: "wall property"
        }
    return names[castle_type]



###### mapping types to examples in any language

def get_examples(castle_type: CastleType, language: Language) -> str:
    if language == Language.GERMAN:
        # to translate in german
        examples = {
            CastleType.COLOR: "grey, red, blue, ...",
            CastleType.MERLON: "split_merlon, rounded_merlon, rectangular_merlon",
            CastleType.LIST: "[element_1, element_2, element_3]",
            CastleType.DRAWBRIDGE_STATE: "opened, closed",
            CastleType.WALL_BORDER: "borders, no_borders",
            CastleType.WALL_PROPERTY: "ivy, window, door, nothing, ..."
        }
    elif language == Language.ITALIAN:
        examples = {
            CastleType.COLOR: "grigio, rosso, blu, ...",
            CastleType.MERLON: "merlo_diviso, merlo_arrotondato, merlo_rettangolare",
            CastleType.LIST: "[elemento_1, elemento_2, elemento_3]",
            CastleType.DRAWBRIDGE_STATE: "aperto, chiuso",
            CastleType.WALL_BORDER: "con_bordi, senza_bordi",
            CastleType.WALL_PROPERTY: "edera, finestra, porta, niente, ..."
        }
    else:
        # english version
        examples = {
            CastleType.COLOR: "grey, red, blue, ...",
            CastleType.MERLON: "split_merlon, rounded_merlon, rectangular_merlon",
            CastleType.LIST: "[element_1, element_2, element_3]",
            CastleType.DRAWBRIDGE_STATE: "opened, closed",
            CastleType.WALL_BORDER: "borders, no_borders",
            CastleType.WALL_PROPERTY: "ivy, window, door, nothing, ..."
        }
    return examples[castle_type]


##### cardinal numbers in any language (up to six)

def get_cardinal_number(num: int, language: Language) -> str:
    if language == Language.GERMAN:
        cardinal_numbers = ["first", "second", "third", "fourth", "fifth", "sixth"]
    elif language == Language.ITALIAN:
        cardinal_numbers = ["primo", "secondo", "terzo", "quarto", "quinto", "sesto"]
    else:
        cardinal_numbers = ["first", "second", "third", "fourth", "fifth", "sixth"]
    return cardinal_numbers[num]



# generates an error message stating that function `func` expects 
# a type `castle_type` as parameter `parameter_position`
# `argument_position` is an integer number and should be 0 for the first parameter
# `castle_type` is one of CastleType (CastleType.COLOR, ...)
# `language` should be one of Languages
def arguments_error_message(func, argument_position: int, castle_type: CastleType) -> str:
    # always in english for now
    func_name = func.__name__
    error_msg = "Invalid arguments in " + func_name + ": \n"

    error_msg += "The " + get_cardinal_number(argument_position, Language.ENGLISH) + " argument should be a " + get_name(castle_type, Language.ENGLISH) + ".\n"
    error_msg +=  "Valid examples: " + get_examples(castle_type, Language.ENGLISH)
    return error_msg
