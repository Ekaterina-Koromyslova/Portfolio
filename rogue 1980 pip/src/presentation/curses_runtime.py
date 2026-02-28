"""
Настройка и запуск curses-среды:

Модуль отвечает за:
- проверка размера терминала (мин 80х24);
- создание базового layout(окна, сообщения, карта, статус);
- инициализация режима curses и цветовых пар;
- запуск приложения через curses.wrapper();
"""
import curses

# TO DO: сделать один модуль с константами

SCREEN_HEIGHT = 24
SCREEN_WIDTH = 80

MESSAGE_LINE_INDEX = 0
MAP_START_LINE_INDEX = 1
MAP_HEIGHT = 22
STATUS_LINE_INDEX = 23


def create_layout(screen: "curses.window"):
    """
    Создает layout окон:
    - окно сообщения;
    - окно карты;
    - окно статуса.
    """
    terminal_height, terminal_width = screen.getmaxyx()

    if terminal_height < SCREEN_HEIGHT or terminal_width < SCREEN_WIDTH:
        raise RuntimeError("Terminal must be at least 80x24")

    message_window = curses.newwin(1, SCREEN_WIDTH, MESSAGE_LINE_INDEX, 0)
    map_window = curses.newwin(MAP_HEIGHT, SCREEN_WIDTH, MAP_START_LINE_INDEX, 0)
    status_window = curses.newwin(1, SCREEN_WIDTH, STATUS_LINE_INDEX, 0)

    return map_window, status_window, message_window

def init_curses():
    """
    Выполняет базовую настройку режима curses.
    """
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.use_default_colors()

def init_colors():
    """
    Инициализирует цветовые пары.
    """
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_WHITE, -1)
    curses.init_pair(4, curses.COLOR_YELLOW, -1)

def run_curses(main_fn):
    """
    Запускает приложение в безопасной оболочке.
    """
    curses.wrapper(main_fn)
