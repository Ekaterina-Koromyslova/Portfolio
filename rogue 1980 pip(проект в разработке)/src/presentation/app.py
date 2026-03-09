"""
Точка входа в приложение.
Отвечает за инициализацию cures, создание окон интерфейса
и управление переходами между экранами.
"""

import curses

from src.presentation import curses_runtime
from src.presentation.input.controller import InputController
from src.presentation.screens.game_screen import GameScreen
from src.presentation.screens.menu_screen import MenuScreen, MenuResult
from src.presentation.screens.stats_screen import StatsScreen

def main(screen: "curses.window") -> None:
    """
    Главная точка входа.
    Выполняет инициализацию curses, создает layout окон
    и управляет основным циклом экранов.
    """
    curses_runtime.init_curses()
    curses_runtime.init_colors()

    map_window, status_window, message_window = curses_runtime.create_layout(screen)
    map_window.keypad(True)

    controller = InputController()

    while True:
        menu_screen = MenuScreen(map_window, status_window, message_window)
        run_screen(controller, map_window, menu_screen)

        if menu_screen.selected == MenuResult.NEW_GAME:
            game_screen = GameScreen(map_window, status_window, message_window)
            run_screen(controller, map_window, game_screen)

        elif menu_screen.selected == MenuResult.LOAD_GAME:
            game_screen = GameScreen(map_window, status_window, message_window)
            run_screen(controller, map_window, game_screen)

        elif menu_screen.selected == MenuResult.SCOREBOARD:
            stats_screen = StatsScreen(map_window, status_window, message_window)
            run_screen(controller, map_window, stats_screen)

        else:
            break


def run_screen(controller: InputController, map_window, screen_obj) -> None:
    """
    Запускает цикл обработки конкретного экрана.
    Обрабатывает ввод пользователя и вызывает методы draw()
    и handle() у переданного объекта экрана до тех пор,
    пока экран не завершит работу.
    """
    is_running = True
    while is_running:
        screen_obj.draw()
        action, pressed_key_code = controller.read(map_window)
        is_running = screen_obj.handle(action, pressed_key_code)
        screen_obj.draw()

def run() -> None:
    """
    Запускает приложение в режиме curses.
    """
    curses_runtime.run_curses(main)
