"""
Модуль отображения строки сообщений игроку.

Содержит простой лог сообщений, который хранит 1
строку текста и выводит ее в отдельное окно curses.
"""
import curses


class MessageLog:
    """
    Компонент для хранения и отображения текущего сообщения
    игроку.

    Используется для вывода подсказок и статуса действий.
    """
    def __init__(self) -> None:
        """ Создает пустой лог сообщений. """
        self._text = ""

    def set(self, text: str) -> None:
        """ Устанавливает текст текущего сообщения. """
        self._text = text

    def render(self, message_window) -> None:
        """Отрисовывает текущее сообщение."""
        message_window.erase()
        try:
            message_window.addstr(0, 0, self._text)
        except curses.error:
            pass
        message_window.refresh()
