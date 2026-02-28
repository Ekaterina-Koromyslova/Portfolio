"""
Модуль с маппингом клавиатуры.
"""

QUIT = "QUIT"
MOVE_UP = "MOVE_UP"
MOVE_DOWN = "MOVE_DOWN"
MOVE_LEFT = "MOVE_LEFT"
MOVE_RIGHT = "MOVE_RIGHT"
NOOP = "NOOP"

KEY_TO_ACTION = {
    ord("q"): QUIT,
    ord("Q"): QUIT,

    ord("w"): MOVE_UP,
    ord("W"): MOVE_UP,
    ord("s"): MOVE_DOWN,
    ord("S"): MOVE_DOWN,
    ord("a"): MOVE_LEFT,
    ord("A"): MOVE_LEFT,
    ord("d"): MOVE_RIGHT,
    ord("D"): MOVE_RIGHT,
}
