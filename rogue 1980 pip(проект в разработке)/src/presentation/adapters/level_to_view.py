"""
Адаптер преобразования доменной модели уровня в представление для рендера.

Преобразует объекты Level (rooms, passages, items)
в простые структуры данных (grid, items, doors, keys),
которые используются слоем presentation.
"""

from src.domain.entities.entities import ItemType

def build_view_state(level) -> tuple[list[list[str]], list[dict], list[dict], list[dict]]:
    """
    Строит представление уровня для слоя отображения.
    """
    max_x = 0
    max_y = 0

    for room in level.rooms:
        pos = room.position
        max_x = max(max_x, pos.x + pos.dx)
        max_y = max(max_y, pos.y + pos.dy)

    for passage in level.passages:
        for p in passage.passage:
            max_x = max(max_x, p.x + 1)
            max_y = max(max_y, p.y + 1)

    grid = [["#" for _ in range(max_x)] for _ in range(max_y)]

    for room in level.rooms:
        pos = room.position
        for y in range(pos.y, pos.y + pos.dy):
            for x in range(pos.x, pos.x + pos.dx):
                grid[y][x] = "."

    for passage in level.passages:
        for p in passage.passage:
            grid[p.y][p.x] = "."

    items = []
    keys = []

    for room in level.rooms:
        for item_type, item_list in room.items.storage.items():
            for item_in_room in item_list:
                pos = item_in_room.position

                if item_type == ItemType.KEY:
                    keys.append({"y": pos.y, "x": pos.x})
                else:
                    items.append({
                        "y": pos.y,
                        "x": pos.x,
                        "type": item_type
                    })

    doors = []
    for passage in level.passages:
        if passage.is_locked:
            doors.append({
                "y": passage.entrance.y,
                "x": passage.entrance.x,
                "is_open": False
            })

    return grid, items, doors, keys
