"""
Экран статистики (Scoreboard).

В текущей версии выводит заглушку и используется для
демонстрации перехода к отдельному экрану.
"""
import curses

from src.presentation.widgets.message_log import MessageLog
from src.presentation.widgets.statusbar import StatusBar
from src.presentation.input.keymap import QUIT, NOOP


class StatsScreen:
    """ Экран отображения статистики. Пока реализован как заглушка. """   
    def __init__(
        self,
        map_window: "curses.window",
        status_window: "curses.window",
        message_window: "curses.window",
    ) -> None:
        """
        Инициализирует экран статистики и подготавливает сообщения.
        """
        self.map_window = map_window
        self.status_window = status_window
        self.message_window = message_window

        self.message_log = MessageLog()
        self.status_bar = StatusBar()
        self.message_log.set("Scoreboard (stub). Press q to return.")

    def draw(self) -> None:
        """
        Отрисовывает интерфейс экрана статистики.
        """
        self.status_bar.render(self.status_window)
        self.map_window.erase()
        self.map_window.box()
        self.map_window.addstr(2, 2, "SCOREBOARD")
        self.map_window.refresh()
        self.message_log.render(self.message_window)

    def handle(self, action, pressed_key_code) -> bool:
        """
        Обрабатывает ввод пользователя.
        False - выход с экрана, иначе True.
        """
        _ = pressed_key_code

        if action == QUIT:
            return False
        if action == NOOP:
            return True
        return True
