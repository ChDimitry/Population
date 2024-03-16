from enum import Enum

class Decision(Enum):
    MOVE_UP = 'move_up'
    MOVE_DOWN = 'move_down'
    MOVE_LEFT = 'move_left'
    MOVE_RIGHT = 'move_right'
    DO_NOTHING = 'do_nothing'
    GO_CHARGE = 'go_charge'
