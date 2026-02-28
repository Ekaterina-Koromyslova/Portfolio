"""
Туман войны
- visible_mask: что видно сейчас
- seen_mask: что было увидено ранее
"""
def point_inside_room(x: int, y: int, room: dict[int, str]) -> bool:
    """
    Проверяет находится ли точка внутри прямоуг. комнаты, вкл. границы.
    """
    return (
        room["x"] <= x <= room["x"] + room["w"] - 1
        and room["y"] <= y <= room["y"] + room["h"] - 1
    )

def point_inside_room_interior(x: int, y: int, room: dict[int, str]) -> bool:
    """
    Проверяет находится ли точка внутри прямоуг. комнаты, не вкл. границы.
    """
    return (
        room["x"] + 1 <= x <= room["x"] + room["w"] - 2
        and room["y"] + 1 <= y <= room["y"] + room["h"] - 2
    )

def get_room_index_by_coord(x: int, y: int, rooms: dict[int, str]) -> int:
    """
    Возвращает индекс комнаты в которой находится точка, либо -1 если точка вне
    """
    for i, room in enumerate(rooms):
        if point_inside_room(x, y, room):
            return i
    return -1

def is_vertical_direction(player_x: int, player_y: int, room: dict[str, int]) -> bool:
    """
    Определяет ориентацию открытия комнаты: вертикальная/горизонтальная.
    """
    right_inside = point_inside_room_interior(player_x + 1, player_y, room)
    left_inside = point_inside_room_interior(player_x - 1, player_y, room)
    return (not right_inside) and (not left_inside)

def reveal_room_full(seen_mask: list[list[bool]], room: dict[str, int]) -> None:
    """Открывает комнату полностью"""
    for y in range(room["y"] + 1, room["y"] + room["h"] - 1):
        for x in range(room["x"] + 1, room["x"] + room["w"] - 1):
            seen_mask[y][x] = True

def reveal_room_partial(
        visible_mask: list[list[bool]],
        seen_mask: list[list[bool]],
        player_x: int,
        player_y: int,
        room: dict[str,int],
    ) -> None:
    """
    Частично открывает комнату
    """
    vertical = is_vertical_direction(player_x, player_y, room)

    for y in range(room["y"] + 1, room["y"] + room["h"] - 1):
        for x in range(room["x"] + 1, room["x"] + room["w"] - 1):
            dx = x - player_x
            dy = y - player_y

            if vertical and abs(dx) >= abs(dy):
                visible_mask[y][x] = True
                seen_mask[y][x] = True
            elif (not vertical) and abs(dx) <= abs(dy):
                visible_mask[y][x] = True
                seen_mask[y][x] = True

def compute_fog(grid: list[list[str]],
                rooms: list[dict[str, int]],
                seen_rooms: list[bool],
                player_x: int,
                player_y: int,
                seen_mask: list[list[bool]],
                ) -> list[list[bool]]:
    """
    Вычисляет visible_mask (что видно прямо сейчас) и обновляет seen_mask/seen_rooms.
    """
    height = len(grid)
    width = len(grid[0])

    visible_mask = []
    for _ in range(height):
        visible_mask.append([False] * width)

    player_room_index = get_room_index_by_coord(player_x, player_y, rooms)

    for i, room in enumerate(rooms):
        if i != player_room_index and seen_rooms[i]:
            reveal_room_full(seen_mask, room)

    if player_room_index != -1:
        room = rooms[player_room_index]
        reveal_room_partial(visible_mask, seen_mask, player_x, player_y, room)
        seen_rooms[player_room_index] = True

    return visible_mask
