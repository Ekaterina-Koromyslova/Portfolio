import random
from src.domain.entities.entities import Item, MonsterType, StatType, ItemType
from domain.entities import Position, MonsterDict, Monster, ItemInRoom
from domain.entities import Player, Room, Passage, Level, BaseParam, Entity
from dataclasses import dataclass

@dataclass(frozen=True)
class FConst:
    INITIAL_HIT_CHANCE = 70
    STANDARD_AGILITY = 50
    AGILITY_FACTOR = 0.3
    INITIAL_DAMAGE = 30
    STANDARD_STRENGTH = 50
    STRENGTH_FACTOR = 0.3
    STRENGTH_ADDITION = 65
    SLEEP_CHANCE = 15
    MAX_HP_PART = 10
    LOOT_AGILITY_FACTOR = 0.2
    LOOT_HP_FACTOR = 0.5
    LOOT_STRENGTH_FACTOR = 0.5
    MAXIMUM_FIGHTS = 8

class Battle:
    __slots__ = ('monster', 'is_attack', 'is_finish')
    def __init__(self, monster: Monster, is_attack):
        self.monster = monster
        self.monster.is_first_hit = True
        self.monster.is_resting = False
        self.is_attack = is_attack
        self.is_finish = False
        #self.is_killed = False

class BattlePicture:
    __slots__ = ('attacks_monsters', 'hit_back_monsters', 'killed_monsters',
                 'num_attacks', 'num_hit_back', 'num_killed')
    def __init__(self):
        self.attacks_monsters = []
        self.num_attacks = 0
        self.hit_back_monsters = []
        self.num_hit_back = 0
        self.killed_monsters = []
        self.num_killed = 0

    def add_battle(self, new_battle: Battle):
        if new_battle.is_attack:
            self.attacks_monsters.append(new_battle)
            self.num_attacks += 1
        else:
            self.hit_back_monsters.append(new_battle)
            self.num_hit_back += 1

    def del_battle(self, new_battle: Battle):
        if new_battle.is_finish: # and new_battle.is_killed:
            if new_battle.is_attack:
                if new_battle in self.attacks_monsters:
                    self.attacks_monsters.remove(new_battle)
                    self.num_attacks -= 1
            else:
                if new_battle in self.hit_back_monsters:
                    self.hit_back_monsters.remove(new_battle)
                    self.num_hit_back -= 1
            if new_battle not in self.killed_monsters:
                self.killed_monsters.append(new_battle)
                self.num_killed += 1

"""
    @brief Функция расчета количества золота с уровня.
"""
def calculation_loot(monster: Entity):
    if isinstance(monster, Monster):
        gold = (monster.stats.agility * FConst.LOOT_AGILITY_FACTOR +
                monster.stats.health * FConst.LOOT_HP_FACTOR +
                monster.stats.strength * FConst.LOOT_STRENGTH_FACTOR +
                random.randrange(20))

        #base_gold = monster.stats.health // 10 + monster.stats.strength // 5
        #coef = 1 + monster.hostility*monster.stats.agility / 100
        #return int(coef*base_gold)
        return int(gold)
    return -1
"""! После боя восстановить флаг вампира defender.is_first_hit = True
"""
def is_hit_to_goal(attacker: Entity, defender: Entity):
    if defender.type == MonsterType.VAMPIRE and defender.is_first_hit:
        defender.is_first_hit = False
        return False

    chance_to_hit = attacker.stats.agility - defender.stats.agility + 50
    chance_to_hit = max(5, min(95, chance_to_hit))
    if attacker.type != MonsterType.OGRE and random.randint(1,100) > chance_to_hit:
        return False

    if attacker.type == MonsterType.OGRE:
        attacker.is_resting = True

    return True

def damage_calc(attacker: Entity, defender: Entity):
    damage0 = FConst.INITIAL_DAMAGE
    if attacker.type == MonsterType.PLAYER:
        if attacker.weapon.type == ItemType.NONE:
            damage = damage0 + (attacker.stats.strength - FConst.STANDARD_STRENGTH)*FConst.STRENGTH_FACTOR
        else:
            damage = attacker.weapon.strength*(attacker.stats.strength + FConst.STRENGTH_ADDITION) / 100
    else:
        if attacker.type != MonsterType.VAMPIRE:
            damage = (attacker.stats.strength - FConst.STANDARD_STRENGTH)*FConst.STRENGTH_FACTOR
            if attacker.type != MonsterType.OGRE:
                damage += damage0
        else:
            damage = defender.regen_limit / FConst.MAX_HP_PART

    return int(damage)
"""
    @detail Одиночный удар по персонажу.
    @return gold, damage. Возможны исходы: -1, damage — монстр убил игрока,
        0, damage — если оба живы(damage = 0 в случае промаха, в случае пропуска damage = -1),
        gold, damage - если выиграл игрок;
"""
def calc_attack_result(attacker: Entity, defender: Entity):
    if attacker.is_resting:
        attacker.is_resting = False
        return 0, -1

    damage = 0
    if is_hit_to_goal(attacker, defender):
        damage = damage_calc(attacker, defender)
        is_dead = defender.take_damage(damage)

        # вампир ворует здоровье максимальное при успешном ударе
        if attacker.type == MonsterType.VAMPIRE and defender.type == MonsterType.PLAYER:
            defender.regen_limit = max(1, defender.regen_limit - 1)

        # змей может заморозить игрока на ход
        if attacker.type == MonsterType.SNAKE and defender.type == MonsterType.PLAYER:
            if random.random() < FConst.SLEEP_CHANCE / 100:
                defender.is_resting = True

        # проверка смерти обороняющейся стороны
        if is_dead:
            if isinstance(attacker, Player) and defender.type != MonsterType.PLAYER:
                gold = calculation_loot(defender)
                if gold > 0:
                    attacker.money += gold
                return gold, damage
            elif defender.type == MonsterType.PLAYER:
                return -1, damage

    return 0, damage

def is_equal_x_y(pos1: Position, pos2: Position):
    return pos1.x == pos2.x and pos1.y == pos2.y

def is_gv_neighbor(pos1: Position, pos2: Position):
    return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y) == 1

def is_neighbor(pos1: Position, pos2: Position):
    return max(abs(pos1.x - pos2.x), abs(pos1.y - pos2.y)) == 1

def is_contact(pos: Position, monster: Monster):
    return is_neighbor(pos, monster.position)





def find_nearest_monsters(player: Player, level: Level):
    monsters = []
    for room in level.rooms:
        if room.is_visited:
            for monster in room.monsters:
                if is_gv_neighbor(monster.position, player.position):
                    monsters.append(monster)

    return monsters






            

#def find_monster_to_attack(player: Player, level: Level):
#    for

def attack_procedure(player: Player, battle_picture: BattlePicture, choose_buttle: Battle):

    result = []
    if  battle_picture.attacks_monsters:
        for battle in battle_picture.attacks_monsters:
            if battle.is_attack and not battle.is_finish:
                gold, damage = calc_attack_result(battle.monster, player)
                result.append([gold, damage])
                if gold == -1:
                    return result

    if choose_buttle and (choose_buttle in battle_picture.attacks_monsters or choose_buttle in
                          battle_picture. hit_back_monsters):
        gold, damage = calc_attack_result(player, choose_buttle.monster)
        result.append([gold, damage])
        if gold > 0:
            choose_buttle.is_finish = True
            battle_picture.del_battle(choose_buttle)

    #for battle in battle_picture.hit_back_monsters:
    #    if not battle.is_finish:
    #        gold, damage = calc_attack_result(battle.monster, player)
    #        result.append([gold, damage])
    #        if gold == -1:
    #            return result

    return result

#сканируем окружение на предмет контакта, если он есть создаем битву и

"""
def calc_attack_result(attacker: Entity, defender: Entity):
    if defender.type == MonsterType.VAMPIRE:
        if defender.is_first_hit:
            defender.is_first_hit = False
            return 0, 0

    if attacker.type == MonsterType.OGRE and attacker.is_resting:
            attacker.is_resting = False
            return 0, 0

    chance_to_hit = attacker.stats.agility - defender.stats.agility + 50
    if random.randint(1,100) > chance_to_hit: # промах
        # после промаха огр все равно отдыхает
        if attacker.type == MonsterType.OGRE:
            attacker.is_resting = True
        return 0, 0

    w_damage = attacker.weapon.strength if attacker.weapon.type == ItemType.WEAPON else 2
    t_damage = (w_damage + random.randint(1,6))*(1 + attacker.stats.strength /100)
    t_damage = int(t_damage)

    is_dead = defender.take_damage(t_damage)
    # вампир ворует здоровье максимальное при успешном ударе
    if attacker.type == MonsterType.VAMPIRE and defender.type == MonsterType.PLAYER:
        defender.regen_limit = max(1, defender.regen_limit - 1)
    # после успешной атаки огр отдыхает
    if attacker.type == MonsterType.OGRE: attacker.is_resting = True

    if is_dead:
        # игрок выиграл
        if isinstance(attacker, Player) and defender.type != MonsterType.PLAYER:
            gold = calculation_loot(defender)
            if gold > 0:
                attacker.money += gold
            return gold, t_damage
        # игрок проиграл
        elif defender.type == MonsterType.PLAYER:
            return -1, t_damage
    # змей может заморозить игрока на ход
    if attacker.type == MonsterType.SNAKE and defender.type == MonsterType.PLAYER:
        if random.random() < 0.2:
            defender.is_resting = True

    return 0, t_damage
"""

