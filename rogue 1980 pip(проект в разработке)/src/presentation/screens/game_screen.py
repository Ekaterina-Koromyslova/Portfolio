"""
Основной экран игры.

Отвечает за отображение уровня, обработку ввода игрока
и взаимодействие с UI-виджетами.
"""
import curses
from src.presentation.render.renderer import render_map
from src.presentation.widgets.message_log import MessageLog
from src.presentation.widgets.statusbar import StatusBar
from src.presentation.input.keymap import (
    QUIT, MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, NOOP
)
from src.presentation.widgets.inventory import InventoryWidget
from src.domain.entities.entities import Level, Player
from src.presentation.adapters.level_to_view import build_view_state
from src.domain.generation.generator import generate_next_level


class GameScreen:
    """
    Экран игрового процесса.

    Инициализирует уровень через доменный генератор, строит представление для
    рендера, рисует карту и обрабатывает перемещения/команды игрока.
    """
    def __init__(
        self,
        map_window: "curses.window",
        status_window: "curses.window",
        message_window: "curses.window",
    ) -> None:
        """Создает игровой экран и генерирует стартовый уровень"""
        self.map_window = map_window
        self.status_window = status_window
        self.message_window = message_window

        self.message_log = MessageLog()
        self.status_bar = StatusBar()

        window_height, window_width = self.map_window.getmaxyx()
        self.window_height = window_height
        self.window_width = window_width

        self.level = Level()
        self.player = Player()
        generate_next_level(self.level, self.player)

        self.grid, self.items, self.doors, self.keys = build_view_state(self.level)

        inner_height = len(self.grid)
        inner_width = len(self.grid[0])
        self.visible_mask = [[True] * inner_width for _ in range(inner_height)]
        self.seen_mask = [[False] * inner_width for _ in range(inner_height)]


        self.player_y = self.player.stats.position.y
        self.player_x = self.player.stats.position.x

        self.message_log.set("Keys: q=quit, WASD=move")

        # инвентарь пока что тестовый
        self.inventory_items = self.create_test_inventory_items()
        self.inventory_widget = None

    def create_test_inventory_items(self) -> list[dict[str, object]]:
        """Создает тестовый набор инвентаря."""
        return [
            {"name": "Potion of healing", "quantity": 2},
            {"name": "Scroll of identify", "quantity": 1},
            {"name": "Ration of food", "quantity": 3},
            {"name": "Gold coins", "quantity": 87},
            {"name": "Dagger", "quantity": 1},
        ]

    def _is_inventory_key(self, key_code: int) -> bool:
        """Проверка клавиши открытия/закрытия инвентаря"""
        if 0 <= key_code < 256:
            pressed_character = chr(key_code)
            return pressed_character == "i" or pressed_character == "I"
        return False

    def draw(self) -> None:
        """Отрисовывает игру или активный виджет"""
        if self.inventory_widget is not None:
            self.inventory_widget.draw()
            return

        self.status_bar.render(self.status_window)

        render_map(
            self.map_window,
            self.grid,
            self.player_y,
            self.player_x,
            self.items,
            self.doors,
            self.keys,
            self.visible_mask,
            self.seen_mask,
        )

        self.message_log.render(self.message_window)

    def handle(self, action, pressed_key_code) -> bool:
        """
        Обрабатывает ввод игрока.
        Возвращает False, если нужно выйти из игрового экрана.
        """
        if self.inventory_widget is not None:
            user_interface_action = self.inventory_widget.handle(action, pressed_key_code)

            if user_interface_action.action_type == "close_inventory":
                self.inventory_widget = None
                self.message_log.set("Inventory closed")
                return True

            if user_interface_action.action_type == "use_item":
                selected_item = user_interface_action.action_payload

                if isinstance(selected_item, dict):
                    selected_item_name = selected_item.get("name", "item")
                else:
                    selected_item_name = str(selected_item)

                self.message_log.set(f"Use item: {selected_item_name}")
                self.inventory_widget = None
                return True

            return True

        if self._is_inventory_key(pressed_key_code):
            self.inventory_widget = InventoryWidget(
                self.map_window,
                self.status_window,
                self.message_window,
                self.inventory_items,
            )
            self.message_log.set("Inventory opened")
            return True

        if action == QUIT:
            return False

        new_y = self.player_y
        new_x = self.player_x

        if action == MOVE_UP:
            new_y -= 1
        elif action == MOVE_DOWN:
            new_y += 1
        elif action == MOVE_LEFT:
            new_x -= 1
        elif action == MOVE_RIGHT:
            new_x += 1
        elif action == NOOP:
            pass

        inner_top = 1
        inner_left = 1
        inner_bottom = self.window_height - 2
        inner_right = self.window_width - 2

        can_move_by_bounds = (
            inner_top <= new_y <= inner_bottom
            and inner_left <= new_x <= inner_right
        )

        moved = False
        if can_move_by_bounds:
            grid_y = new_y - 1
            grid_x = new_x - 1
            if self.grid[grid_y][grid_x] != "#":
                self.player_y = new_y
                self.player_x = new_x
                moved = True

        if 0 <= pressed_key_code < 256:
            key_text = chr(pressed_key_code)
        else:
            key_text = str(pressed_key_code)

        if moved:
            self.message_log.set(f"Moved with {key_text} (q=quit)")
        else:
            self.message_log.set(f"Pressed {key_text} (q=quit)")

        return True
