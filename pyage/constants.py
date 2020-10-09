from enum import IntEnum, auto, unique


@unique
class EVENT(IntEnum):

    KEY = auto()
    FOCUS = auto()
