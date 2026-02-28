import enum

class Dimension(enum.Enum):
    X = 0           # вдоль оси X
    Y = 1           # вдоль оси Y
    Coord_Num = 2

class MonsterType(enum.Enum):
    ZOMBIE = 0          # зомби
    VAMPIRE = 1         # вампир
    GHOST = 2           # призрак
    OGRE = 3            # огр
    SNAKE = 4           # змей

class HostilityType(enum.Enum):
    LOW = 0             # круг адиусом LOW_HOSTILITY_RADIUS
    AVERAGE = 1         # круг адиусом AVERAGE_HOSTILITY_RADIUS
    HIGH = 2            # круг адиусом HIGH_HOSTILITY_RADIUS

class StatType(enum.IntEnum):
    HEALTH = 0          # здоровье
    AGILITY = 1         # ловкость
    STRENGTH = 2        # сила
    HOSTILITY = 3
    NONE = -1

class ItemType(enum.IntEnum):
    NONE = 0            # ничего
    FOOD = 1            # еда
    ELIXIR = 2          # эликсир
    WEAPON = 3          # оружие
    SCROLL = 4          # свиток
    TREASURE = 5        # сокровище
    KEY = 6             # ключ

class Directions(enum.IntEnum):
    FORWARD = 0         # вперед
    BACK = 1            # назад
    LEFT = 2            # влево
    RIGHT = 3           # вправа
    D_FORWARD_LEFT = 4  # влево вверх диагонально
    D_FORWARD_RIGHT = 5 # вправо вверх диагонально
    D_BACK_LEFT = 6     # влево вниз диагонально
    D_BACK_RIGHT = 7    # вправо вниз диагонально
    STOP = 8            # не двигаться

class Position:
    __slots__ = ('x', 'y', 'dx', 'dy')
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
    def change_position(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

class Item:
    def __init__(self, _type, _subtype = 0, _health = 0, _agility = 0, _strength = 0, _value = 0,
                 _duration=0, _name = ''):
        self.type = _type
        self.subtype = _subtype
        self.health = _health
        self.maximum_health = _health
        self.agility = _agility
        self.strength = _strength
        self.duration = _duration
        self.value = _value
        self.name = _name

class ItemInRoom:
    __slots__ = ('item', 'position')
    def __init__(self, item: Item, position: Position):
        self.item = item
        self.position = position

class Character:
    __slots__ = ('position', 'health', 'agility', 'strength')
    def __init__(self):
        self.position = Position()    # координаты персонажа
        self.health = 100                # текущие показатели ловкости
        self.agility = 50                # показатель ловкости
        self.strength = 60              # показатель силы
    def restore(self, pos: Position, health: float, agility: int, strength:int):
        self.position = pos       # координаты персонажа
        self.health = health            # текущие показатели ловкости
        self.agility = agility          # показатель ловкости
        self.strength = strength

class MonsterDict:
    stats = {
        MonsterType.ZOMBIE: {StatType.HEALTH: 50, StatType.AGILITY: 25, StatType.STRENGTH: 125, StatType.HOSTILITY: 1},
        MonsterType.VAMPIRE: {StatType.HEALTH: 50, StatType.AGILITY: 75, StatType.STRENGTH: 125, StatType.HOSTILITY: 2},
        MonsterType.GHOST: {StatType.HEALTH: 75, StatType.AGILITY: 75, StatType.STRENGTH: 25, StatType.HOSTILITY: 0},
        MonsterType.OGRE: {StatType.HEALTH: 150, StatType.AGILITY: 25, StatType.STRENGTH: 100, StatType.HOSTILITY: 1},
        MonsterType.SNAKE: {StatType.HEALTH: 100, StatType.AGILITY: 100, StatType.STRENGTH: 30, StatType.HOSTILITY: 2}
    }

class Monster:
    __slots__ = ('type', 'health', 'agility', 'strength', 'hostility', 'is_chasing', 'direction', 'position')
    def __init__(self):
        self.type = -1
        self.health = 0
        self.agility = 0
        self.strength = 0
        self.hostility = 0
        self.is_chasing = False
        self.direction = Directions.STOP
        self.position = Position()
    def change_stats(self, health, agility, strength, hostility):
        self.health = health
        self.agility = agility
        self.strength = strength
        self.hostility = hostility
    def change_position(self, new_position: Position):
        self.position = new_position
    def change_direction(self, new_direction: Directions):
        self.direction = new_direction

class ItemsInRoom:
    __slots__ = ('food_num', 'elixir_num', 'scroll_num', 'weapon_num', 'treasure_num', 'max_item', 'total_sum', 'storage')
    TYPE_DICT = {
        ItemType.FOOD: 'food_num',
        ItemType.ELIXIR: 'elixir_num',
        ItemType.SCROLL: 'scroll_num',
        ItemType.WEAPON: 'weapon_num',
        ItemType.TREASURE: 'treasure_num'
    }

    def __init__(self):
        for el in self.TYPE_DICT.values():
            setattr(self, el, 0)
        self.max_item = 5
        self.total_sum = 0
        self.storage = {el: [] for el in ItemType}

    def change_num(self, item_type: ItemType, delta: int):
        my_attr = self.TYPE_DICT.get(item_type)
        if my_attr:
            my_val = getattr(self, my_attr) + delta
            setattr(self, my_attr, my_val)

    def add_item(self, item_type: ItemType, item):
        total_in_room = self.total_sum
        if total_in_room < self.max_item or item_type == ItemType.KEY:
            self.storage[item_type].append(item)
            if item_type != ItemType.KEY:
                self.change_num(item_type, 1)
                self.total_sum +=1

    def del_item(self, item_type: ItemType, item_idx: int):
        res = None
        if 0 <= item_idx < len(self.storage[item_type]):
            res = self.storage[item_type].pop(item_idx)
            if item_type != ItemType.KEY:
                self.change_num(item_type, -1)
                self.total_sum -= 1
        return res

class Inventory:
    __slots__ = ('current_size', 'max_category_size', 'storage')
    def __init__(self):
        self.current_size = 0
        self.max_category_size = 9
        self.storage = {
            ItemType.FOOD: [],
            ItemType.ELIXIR: [],
            ItemType.SCROLL: [],
            ItemType.WEAPON: [],
            ItemType.KEY: []
        }
    def add_item(self, item_type: ItemType, item):
        if len(self.storage[item_type]) < self.max_category_size:
            self.storage[item_type].append(item)
            self.current_size += 1
    def del_item(self, item_type: ItemType, item):
        if len(self.storage[item_type]) > 0:
            self.storage[item_type].remove(item)
            self.current_size -= 1

class Buff:
    __slots__ = ('increase', 'effect_end')
    def __init__(self, increase, effect_end):
        self.increase = increase            # на сколько увеличивается параметр
        self.effect_end = effect_end        # время окончания эффекта

class Buffs:
    __slots__ = ('current_health_buff_num', 'current_strength_buff_num',
                 'current_agility_buff_num', 'max_storage', 'storage')
    def __init__(self):
        self.current_health_buff_num = 0
        self.current_strength_buff_num = 0
        self.current_agility_buff_num = 0
        self.max_storage = 9
        self.storage = {
            StatType.AGILITY: [],
            StatType.HEALTH: [],
            StatType.STRENGTH: []
        }
    def activate_buff(self, buff: Buff, buff_type: StatType):
        if len(self.storage[buff_type]) < self.max_storage:
            self.storage[buff_type].append(buff)
            if buff_type == StatType.HEALTH:
                self.current_health_buff_num += 1
            elif buff_type == StatType.STRENGTH:
                self.current_strength_buff_num += 1
            else:
                self.current_agility_buff_num += 1

    def deactivate_buff(self, buff: Buff, buff_type: StatType):
        if len(self.storage[buff_type]) > 0:
            self.storage[buff_type].remove(buff)
            if buff_type == StatType.HEALTH:
                self.current_health_buff_num -= 1
            elif buff_type == StatType.STRENGTH:
                self.current_strength_buff_num -= 1
            else:
                self.current_agility_buff_num -= 1

class Player:
    __slots__ = ('stats', 'regen_limit', 'inventory', 'weapon', 'buffs', 'money')
    def __init__(self):
        self.stats = Character()
        self.regen_limit = self.stats.health
        self.money = 0
        self.inventory = Inventory()
        self.weapon = Item(ItemType.WEAPON)
        self.buffs = Buffs()

    def change(self, stats: Character, health_max: int, inventory: Inventory,
               item: Item, buffs: Buffs, money: int):
        self.stats = stats
        self.regen_limit = health_max
        self.inventory = inventory
        if item.type == ItemType.WEAPON:
            self.weapon = item
        self.buffs = buffs
        self.money = money

class Room:
    __slots__ = ('room_num', 'position', 'width', 'height', 'items', 'item_num', 'monsters', 'monster_num')
    def __init__(self, number):
        self.room_num = number
        self.position = Position()
        self.items = ItemsInRoom()
#        self.item_num = 0
        self.monsters = []
        self.monster_num = 0
    def add_position(self, x: int, y: int, dx: int, dy: int):
        self.position.x = x
        self.position.y = y
        self.position.dx = dx
        self.position.dy = dy
    def add_monster(self, monster: Monster):
        self.monsters.append(monster)
        self.monster_num += 1
"""!
    @brief Класс коридоров, который содержит помимо точек коридора и точку входа.
    @detail При генерации точка входа у нас открыта.
"""
class Passage:
    __slots__ = ('passage', 'is_locked', 'entrance', 'exit', 'key_in_room')
    def __init__(self):
        self.passage = []
        self.is_locked = False
        self.key_in_room = -1
        self.entrance = Position()
        self.exit = Position()
    def add_point(self, poz: Position):
        new_point = Position()
        new_point.change_position(poz.x, poz.y, 1, 1)
        self.passage.append(new_point)
    def change_entrance(self, pos):
        self.is_locked = False
        self.entrance.change_position(pos.x, pos.y, pos.dx, pos.dy)
    def change_exit(self, pos):
        self.is_locked = False
        self.exit.change_position(pos.x, pos.y, pos.dx, pos.dy)

class Level:
    __slots__ = ('init_position', 'end_position', 'entrance', 'exit', 'rooms', 'passages', 'level_num', 'rooms_with_key')
    def __init__(self):
        self.init_position = Position()
        self.entrance = -1
        self.exit = -1
        self.rooms = []
        self.passages = []
        self.level_num = 1
        self.end_position = Position()
        self.rooms_with_key = []
    def add_passage(self, passage: Passage):
        self.passages.append(passage)
        if passage.key_in_room != -1 and passage.key_in_room not in self.rooms_with_key:
            self.rooms_with_key.append(passage.key_in_room)


"""
class Treasure:
    __slots__ = ('value',)
    def __init__(self):
        self.value = 0      # ценность сокровища

class Food:
    __slots__ = ('to_regen', 'name')
    def __init__(self):
        self.to_regen = 0
        self.name = ''

class Elixir:
    __slots__ = ('duration', 'stat_type', 'increase', 'name')
    def __init__(self):
        self.duration = 0
        self.stat_type = StatType.NONE
        self.increase = 0
        self.name = ''

class Scroll:
    __slots__ = ('stat_type', 'increase', 'name')
    def __init__(self):
        self.stat_type = StatType.NONE
        self.increase = 0
        self.name = ''

class Weapon:
    __slots__ = ('strength', 'name')
    def __init__(self):
        self.strength = 0
        self.name = ''

class TreasureInRoom:
    __slots__ = ('treasure', 'position')
    def __init__(self, treasure: Treasure, position: Position):
        self.treasure = treasure
        self.position = position

class FoodInRoom:
    __slots__ = ('food', 'position')
    def __init__(self, food: Food, position: Position):
        self.food = food
        self.position = position

class ElixirInRoom:
    __slots__ = ('elixir', 'position')
    def __init__(self, elixir: Elixir, position: Position):
        self.elixir = elixir
        self.position = position

class ScrollInRoom:
    __slots__ = ('scroll', 'position')
    def __init__(self, scroll: Scroll, position: Position):
        self.scroll = scroll
        self.position = position

class WeaponInRoom:
    __slots__ = ('weapon', 'position')
    def __init__(self, weapon, position):
        self.weapon = weapon
        self.position = position
"""



#        self.max_health = 12.0  # Максимум как в оригинале
#        self.health = 12.0      # Текущее HP
#        self.agility = 1        # Ловкость (базовая)
#        self.strength = 16
#define ROOMS_IN_WIDTH                                       3
#define ROOMS_IN_HEIGHT                                      3
#define ROOMS_NUM           (ROOMS_IN_WIDTH * ROOMS_IN_HEIGHT)
#define MAX_PASSAGE_PARTS                                    3
#define MAX_PASSAGES_NUM ((ROOMS_NUM - 1) * MAX_PASSAGE_PARTS)

#define REGION_WIDTH                     27
#define REGION_HEIGHT                    10
#define MIN_ROOM_WIDTH                    6
#define MAX_ROOM_WIDTH   (REGION_WIDTH - 2)
#define MIN_ROOM_HEIGHT                   5
#define MAX_ROOM_HEIGHT (REGION_HEIGHT - 2)

#define CONSUMABLES_TYPES_NUM                                          4
#define CONSUMABLES_TYPE_MAX_NUM                                       9
#define CONSUMABLES_NUM CONSUMABLES_TYPES_NUM * CONSUMABLES_TYPE_MAX_NUM

#define NO_WEAPON 0

#define MAX_NAME_LEN (32 + 1)

#define MAX_PERCENT_FOOD_REGEN_FROM_HEALTH 20
#define MAX_PERCENT_AGILITY_INCREASE       10
#define MAX_PERCENT_STRENGTH_INCREASE      10

#define MIN_ELIXIR_DURATION_SECONDS 30
#define MAX_ELIXIR_DURATION_SECONDS 60

#define MIN_WEAPON_STRENGTH 30
#define MAX_WEAPON_STRENGTH 50

#define LOW_HOSTILITY_RADIUS     2
#define AVERAGE_HOSTILITY_RADIUS 4
#define HIGH_HOSTILITY_RADIUS    6

#define MAX_CONSUMABLES_PER_ROOM 3
#define MAX_MONSTERS_PER_ROOM    2

#define LEVEL_UPDATE_DIFFICULTY 10
#define PERCENTS_UPDATE_DIFFICULTY_MONSTERS 2

#define LEVEL_NUM 21



#    LOW, ///< Круг радиусом в LOW_HOSTILITY_RADIUS клетки
#    AVERAGE, ///< Круг радиусом в AVERAGE_HOSTILITY_RADIUS клеток
#    HIGH, ///< Круг радиусом в HIGH_HOSTILITY_RADIUS клеток

    # define INITIAL_HIT_CHANCE      70
    # define STANDART_AGILITY        50
    # define AGILITY_FACTOR         0.3
    # define INITIAL_DAMAGE          30
    # define STANDART_STRENGTH       50
    # define STRENGTH_FACTOR        0.3
    # define STRENGTH_ADDITION       65
    # define SLEEP_CHANCE            15
    # define MAX_HP_PART             10
    # define LOOT_AGILITY_FACTOR    0.2
    # define LOOT_HP_FACTOR         0.5
    # define LOOT_STRENGTH_FACTOR   0.5
    # define MAXIMUM_FIGHTS           8