import curses
from src.domain.entities import Level, MonsterType, ItemType, Player


def draw_level_curses(stdscr, level: Level, player: Player):

    for p in level.passages:
        # 1. Отрисовка точек прохода
        for point in p.passage:
            try:
                stdscr.addch(point.y, point.x, '#')
            except curses.error:
                pass

        stdscr.addch(p.exit.y, p.exit.x, 'x')
        stdscr.addch(p.entrance.y, p.entrance.x, 'o')
# 4. Отрисовка ключа
#        if p.key_in_room != -1 and p.passage:
#            # Кладем ключ на первую доступную точку прохода
#            key_pos = p.passage[0]
#            try:
#                stdscr.addch(key_pos.y, key_pos.x, 'K', curses.A_UNDERLINE)
#            except curses.error:
#                pass

    for room in level.rooms:
        pos = room.position
        # Проходим по высоте (dy) и ширине (dx)
        for i in range(pos.dy):
            for j in range(pos.dx):
                curr_y = pos.y + i
                curr_x = pos.x + j
                # Выбираем символ: границы или пол
                if i == 0 or i == pos.dy - 1:
                    char = '-'  # Горизонтальная стена
                elif j == 0 or j == pos.dx - 1:
                    char = '|'  # Вертикальная стена
                else:
                    char = '.'  # Пол комнаты
                # Рисуем углы
                if (i == 0 or i == pos.dy - 1) and (j == 0 or j == pos.dx - 1):
                    char = '+'
                try:
                    stdscr.addch(curr_y, curr_x, char)
                except curses.error:
                    # Если комната не влезает в экран терминала
                    pass

        # Отрисовка монстров в этой комнате
        for monster in room.monsters:
            match monster.type:
                case MonsterType.ZOMBIE:
                    symb = 'Z'
                case MonsterType.VAMPIRE:
                    symb = 'V'
                case MonsterType.GHOST:
                    symb = 'G'
                case MonsterType.OGRE:
                    symb = 'O'
                case MonsterType.SNAKE:
                    symb = 'S'
                case MonsterType.MIMIC:
                    symb = 'M'
            try:
                # Берем координаты монстра напрямую
                stdscr.addch(monster.position.y, monster.position.x, symb, curses.color_pair(3))
            except curses.error:
                pass

            stdscr.addch(monster.position.y, monster.position.x, symb, curses.color_pair(2))

        for item_type, items_list in room.items.storage.items():
            # Выбираем символ в зависимости от типа ключа
            match item_type:
                case ItemType.FOOD:     symb = '%' # Еда
                case ItemType.ELIXIR:   symb = '!' # Эликсир
                case ItemType.SCROLL:   symb = '?' # Свиток
                case ItemType.WEAPON:   symb = '/' # Оружие
                case ItemType.TREASURE: symb = '*' # Сокровище
    #            case ItemType.KEY:      symb = 'k' # Ключ
                case _:                 symb = 'i' # Прочее

            # Отрисовываем каждый предмет из списка данного типа
            for item in items_list:
                try:
                    # Используем координаты конкретного объекта item.position
                    stdscr.addch(item.position.y, item.position.x, symb, curses.color_pair(5))
                except curses.error:
                    pass

    for p in level.passages:
        # 1. Отрисовка точек прохода
        try:
            stdscr.addch(p.exit.y, p.exit.x, 'x')
            stdscr.addch(p.entrance.y, p.entrance.x, 'o')
        except curses.error:
            pass

    stdscr.addch(player.position.y, player.position.x, "@", curses.color_pair(4))

    stdscr.refresh()