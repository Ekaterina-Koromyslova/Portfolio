"""
Рендеринг карты и сущностей

Отвечает за:
- отрисовку символов с учетом цаетовых пар (для врагов)
- отрисовку карты с рамкой и туманом войны
- отрисовку игрока, предметов, дверй и ключей
"""
import curses
from src.presentation.render.tiles import ENEMY_CHAR_TO_COLOR_PAIR_ID
from src.presentation.render.tiles import ITEMS_TILES


def draw_char(map_window, window_y, window_x, char):
    """
    Рисует один символ на карте.
    Для символов врагов добавляет цветовую пару, иначе рисует обычным цветом
    """
    color_pair_id = ENEMY_CHAR_TO_COLOR_PAIR_ID.get(char)
    if color_pair_id is None:
        map_window.addch(window_y, window_x, ord(char))
    else:
        map_window.addch(window_y, window_x, ord(char), curses.color_pair(color_pair_id))


def render_map(
    map_window: "curses.window",
    grid: list[list[str]],
    player_y: int,
    player_x: int,
    items: list[dict],
    doors: list[dict],
    keys: list[dict],
    visible_mask: list[list[bool]],
    seen_mask: list[list[bool]],
    ) -> None:
    """
    Отрисовывает текущий кадр игры.

    Рисует:
    - рамку окна;
    - карту с учетом тумана войны(visible/seen);
    - двери (+ или /), ключи (k), предметы
    - игрока (@)
    """
    map_window.erase()
    map_window.box()

    inner_height = len(grid)
    inner_width = len(grid[0])

    for grid_y in range(inner_height):
        for grid_x in range(inner_width):
            window_y = grid_y + 1
            window_x = grid_x + 1

            if visible_mask[grid_y][grid_x]:
                char_to_draw = grid[grid_y][grid_x]
            elif seen_mask[grid_y][grid_x]:
                char_to_draw = "."
            else:
                char_to_draw = " "

            draw_char(map_window, window_y, window_x, char_to_draw)

    for door in doors:
        door_window_y = door["y"]
        door_window_x = door["x"]
        door_is_open = door["is_open"]

        door_grid_y = door_window_y - 1
        door_grid_x = door_window_x - 1

        if 0 <= door_grid_y < inner_height and 0 <= door_grid_x < inner_width:
            if visible_mask[door_grid_y][door_grid_x]:
                door_char = "/" if door_is_open else "+"
                draw_char(map_window, door_window_y, door_window_x, door_char)

    for key in keys:
        key_window_y = key["y"]
        key_window_x = key["x"]

        key_grid_y = key_window_y - 1
        key_grid_x = key_window_x - 1

        if 0 <= key_grid_y < inner_height and 0 <= key_grid_x < inner_width:
            if visible_mask[key_grid_y][key_grid_x]:
                draw_char(map_window, key_window_y, key_window_x, "k")

    for item in items:
        item_y = item["y"]
        item_x = item["x"]
        item_type = item["type"]

        item_grid_y = item_y - 1
        item_grid_x = item_x - 1

        if 0 <= item_grid_y < inner_height and 0 <= item_grid_x < inner_width:
            if visible_mask[item_grid_y][item_grid_x]:
                item_char = ITEMS_TILES.get(item_type)
                if item_char is not None:
                    draw_char(map_window, item_y, item_x, item_char)

    map_window.addch(player_y, player_x, ord("@"))
    map_window.refresh()
