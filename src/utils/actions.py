from enum import Enum

class Action(Enum):
    UNKNOWN = 0
    INVALID_MOVE = 1
    REVEAL = 2
    NEW_GAME = 3