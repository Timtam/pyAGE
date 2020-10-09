from enum import IntEnum, auto, unique


@unique
class EVENT(IntEnum):

    KEYDOWN = auto()
    KEYUP = auto()
    FOCUS = auto()
