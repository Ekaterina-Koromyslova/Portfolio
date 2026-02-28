from enum import IntEnum, auto


class Direction(IntEnum):
    FORWARD = 0
    BACK = 1
    LEFT = 2
    RIGHT = 3
    DIAG_FWD_LEFT = 4
    DIAG_FWD_RIGHT = 5
    DIAG_BACK_LEFT = 6
    DIAG_BACK_RIGHT = 7
    STOP = 8


class MonsterType(IntEnum):
    ZOMBIE = 0
    VAMPIRE = 1
    GHOST = 2
    OGRE = 3
    SNAKE_MAGE = 4


class HostilityLevel(IntEnum):
    LOW = 0
    AVERAGE = 1
    HIGH = 2


class StatType(IntEnum):
    HEALTH = 0
    AGILITY = 1
    STRENGTH = 2


class ConsumableType(IntEnum):
    NONE = 0
    FOOD = 1
    ELIXIR = 2
    SCROLL = 3
    WEAPON = 4


class TurnOwner(IntEnum):
    PLAYER = 0
    MONSTER = 1


class GameAction(IntEnum):
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    USE_WEAPON = auto()
    USE_FOOD = auto()
    USE_ELIXIR = auto()
    USE_SCROLL = auto()
    SELECT_ITEM_0 = auto()
    SELECT_ITEM_1 = auto()
    SELECT_ITEM_2 = auto()
    SELECT_ITEM_3 = auto()
    SELECT_ITEM_4 = auto()
    SELECT_ITEM_5 = auto()
    SELECT_ITEM_6 = auto()
    SELECT_ITEM_7 = auto()
    SELECT_ITEM_8 = auto()
    SELECT_ITEM_9 = auto()
    MENU_UP = auto()
    MENU_DOWN = auto()
    MENU_CONFIRM = auto()
    ESCAPE = auto()
    NONE = auto()


class GameScene(IntEnum):
    SPLASH = auto()
    MAIN_MENU = auto()
    GAME = auto()
    INVENTORY = auto()
    GAME_OVER_DEATH = auto()
    GAME_OVER_WIN = auto()
    LEADERBOARD = auto()
