"""
Модуль отображения строки статуса игрока.
"""
import curses


class StatusBar:
    """
    Компонент отображения статусной строки игрока.

    В текущей версии выводит заглушку.
    """
    def render(self, status_window) -> None:
        """Отрисовывает текущий статус игрока."""
        status_window.erase()
        try:
            status_window.addstr(0, 0, "HP: --/-- STR: -- AGI: -- LVL: -- GOLD: --")
        except curses.error:
            pass
        status_window.refresh()
