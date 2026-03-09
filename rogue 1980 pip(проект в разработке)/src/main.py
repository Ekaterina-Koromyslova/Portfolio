import os
import curses
from src.presentation.input.controller import InputController
from src.presentation.visualization import draw_level_curses
from src.presentation.screens.menu_screen import MenuScreen, MenuResult
from src.presentation.screens.stats_screen import StatsScreen
from src.domain.entities import (
    Item, Dimension, MonsterType, HostilityType, StatType, ItemType,
    Directions, Position, Character, MonsterDict, Monster, ItemInRoom,
    ItemsInRoom, Inventory, Buff, Buffs, Player, Room, Passage,
    Level, BaseParam, Const, Entity
)
from src.domain.generation import generate_next_level
from src.domain.characters.character_move import (
    move_character_by_direction,
    check_outside_border,
    check_unoccupied_level,
    get_room_number,
)



def init_curses(stdscr):
    curses.curs_set(0)
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Проход
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Вход
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)  # Закрыто
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Открыто
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Ключ


def run_game_loop(stdscr):
    """
    Текущий игровой цикл
    """
    level = Level()
    player = Player()
    position = Position()

    generate_next_level(level, player, position)

    while True:
        stdscr.clear()

        draw_level_curses(stdscr, level, player)

        max_y, max_x = stdscr.getmaxyx()
        help_text = "WASD - move | Q - quit"
        if len(help_text) < max_x:
            stdscr.addstr(0, 0, help_text)

        stdscr.refresh()

        key = stdscr.getch()

        if key in (ord("q"), ord("Q")):
            break

        direction = None

        if key in (ord("w"), ord("W")):
            direction = Directions.LEFT
        elif key in (ord("s"), ord("S")):
            direction = Directions.RIGHT
        elif key in (ord("a"), ord("A")):
            direction = Directions.FORWARD
        elif key in (ord("d"), ord("D")):
            direction = Directions.BACK
        else:
            continue

        position.copy_position(player.position)
        move_character_by_direction(direction, position)

        if check_outside_border(position, level) and check_unoccupied_level(position, level, player):
            player.change_poz(position)

            room_idx = get_room_number(player.position, level)
            if room_idx != 1:
                level.rooms[room_idx].is_visited = True

def run_stats_screen(stdscr):
    """
    запуск экрана стат. через StatsScreen
    """
    height, width = stdscr.getmaxyx()

    status_window = stdscr.derwin(1, width, 0, 0)
    message_window = stdscr.derwin(1, width, height - 1, 0)
    map_window = stdscr.derwin(height - 2, width, 1, 0)

    controller = InputController()
    stats_screen = StatsScreen(map_window, status_window, message_window)

    running = True
    while running:
        stats_screen.draw()
        action, pressed_key_code = controller.read(map_window)
        running = stats_screen.handle(action, pressed_key_code)

def run_menu(stdscr):
    """
    Запуск главного меню через MenuScreen
    """
    height, width = stdscr.getmaxyx()

    status_window = stdscr.derwin(1, width, 0, 0)
    message_window = stdscr.derwin(1, width, height - 1, 0)
    map_window = stdscr.derwin(height - 2, width, 1, 0)

    controller = InputController()
    menu_screen = MenuScreen(map_window, status_window, message_window)

    running = True
    while running:
        menu_screen.draw()
        action, pressed_key_code = controller.read(map_window)
        running = menu_screen.handle(action, pressed_key_code)

    return menu_screen.selected

def main(stdscr):
    init_curses(stdscr)

    while True:
        stdscr.clear()
        stdscr.refresh()

        selected = run_menu(stdscr)

        if selected == MenuResult.NEW_GAME:
            run_game_loop(stdscr)

        elif selected == MenuResult.LOAD_GAME:
            stdscr.clear()
            stdscr.addstr(0, 0, "Load game is not implemented yet. Press any key ...")
            stdscr.refresh()
            stdscr.getch()
        elif selected == MenuResult.SCOREBOARD:
            run_stats_screen(stdscr)
        elif selected == MenuResult.EXIT or selected is None:
            break

if __name__ == "__main__":
    curses.wrapper(main)