from __future__ import annotations

from src.dto.entities import (
    Position, Size, Rect,
    Treasure, Food, Elixir, Scroll, Weapon,
    RoomFood, RoomElixir, RoomScroll, RoomWeapon, RoomConsumables,
    CharacterStats, Monster,
    Buff, ActiveBuffs, Backpack, Player,
    Room, Passage, Level,
    BattleInfo, MapVisibility, SessionStats, GameState,
)
from src.dto.enums import MonsterType, HostilityLevel, StatType, Direction


# === Геометрия ===

def position_to_dict(p: Position) -> dict:
    return {"x": p.x, "y": p.y}


def position_from_dict(d: dict) -> Position:
    return Position(x=d["x"], y=d["y"])


def size_to_dict(s: Size) -> dict:
    return {"w": s.w, "h": s.h}


def size_from_dict(d: dict) -> Size:
    return Size(w=d["w"], h=d["h"])


def rect_to_dict(r: Rect) -> dict:
    return {"pos": position_to_dict(r.pos), "size": size_to_dict(r.size)}


def rect_from_dict(d: dict) -> Rect:
    return Rect(pos=position_from_dict(d["pos"]), size=size_from_dict(d["size"]))


# === Предметы ===

def treasure_to_dict(t: Treasure) -> dict:
    return {"value": t.value}


def treasure_from_dict(d: dict) -> Treasure:
    return Treasure(value=d["value"])


def food_to_dict(f: Food) -> dict:
    return {"to_regen": f.to_regen, "name": f.name}


def food_from_dict(d: dict) -> Food:
    return Food(to_regen=d["to_regen"], name=d["name"])


def elixir_to_dict(e: Elixir) -> dict:
    return {
        "duration": e.duration,
        "stat": int(e.stat),
        "increase": e.increase,
        "name": e.name,
    }


def elixir_from_dict(d: dict) -> Elixir:
    return Elixir(
        duration=d["duration"],
        stat=StatType(d["stat"]),
        increase=d["increase"],
        name=d["name"],
    )


def scroll_to_dict(s: Scroll) -> dict:
    return {"stat": int(s.stat), "increase": s.increase, "name": s.name}


def scroll_from_dict(d: dict) -> Scroll:
    return Scroll(
        stat=StatType(d["stat"]),
        increase=d["increase"],
        name=d["name"],
    )


def weapon_to_dict(w: Weapon) -> dict:
    return {"strength": w.strength, "name": w.name}


def weapon_from_dict(d: dict) -> Weapon:
    return Weapon(strength=d["strength"], name=d["name"])


# === Предметы в комнате ===

def room_food_to_dict(rf: RoomFood) -> dict:
    return {"food": food_to_dict(rf.food), "geometry": rect_to_dict(rf.geometry)}


def room_food_from_dict(d: dict) -> RoomFood:
    return RoomFood(food=food_from_dict(d["food"]), geometry=rect_from_dict(d["geometry"]))


def room_elixir_to_dict(re: RoomElixir) -> dict:
    return {"elixir": elixir_to_dict(re.elixir), "geometry": rect_to_dict(re.geometry)}


def room_elixir_from_dict(d: dict) -> RoomElixir:
    return RoomElixir(elixir=elixir_from_dict(d["elixir"]), geometry=rect_from_dict(d["geometry"]))


def room_scroll_to_dict(rs: RoomScroll) -> dict:
    return {"scroll": scroll_to_dict(rs.scroll), "geometry": rect_to_dict(rs.geometry)}


def room_scroll_from_dict(d: dict) -> RoomScroll:
    return RoomScroll(scroll=scroll_from_dict(d["scroll"]), geometry=rect_from_dict(d["geometry"]))


def room_weapon_to_dict(rw: RoomWeapon) -> dict:
    return {"weapon": weapon_to_dict(rw.weapon), "geometry": rect_to_dict(rw.geometry)}


def room_weapon_from_dict(d: dict) -> RoomWeapon:
    return RoomWeapon(weapon=weapon_from_dict(d["weapon"]), geometry=rect_from_dict(d["geometry"]))


def room_consumables_to_dict(rc: RoomConsumables) -> dict:
    return {
        "foods": [room_food_to_dict(f) for f in rc.foods],
        "elixirs": [room_elixir_to_dict(e) for e in rc.elixirs],
        "scrolls": [room_scroll_to_dict(s) for s in rc.scrolls],
        "weapons": [room_weapon_to_dict(w) for w in rc.weapons],
    }


def room_consumables_from_dict(d: dict) -> RoomConsumables:
    return RoomConsumables(
        foods=[room_food_from_dict(f) for f in d.get("foods", [])],
        elixirs=[room_elixir_from_dict(e) for e in d.get("elixirs", [])],
        scrolls=[room_scroll_from_dict(s) for s in d.get("scrolls", [])],
        weapons=[room_weapon_from_dict(w) for w in d.get("weapons", [])],
    )


# === Персонажи ===

def character_stats_to_dict(cs: CharacterStats) -> dict:
    return {
        "coords": rect_to_dict(cs.coords),
        "health": cs.health,
        "agility": cs.agility,
        "strength": cs.strength,
    }


def character_stats_from_dict(d: dict) -> CharacterStats:
    return CharacterStats(
        coords=rect_from_dict(d["coords"]),
        health=d["health"],
        agility=d["agility"],
        strength=d["strength"],
    )


def monster_to_dict(m: Monster) -> dict:
    return {
        "base_stats": character_stats_to_dict(m.base_stats),
        "type": int(m.type),
        "hostility": int(m.hostility),
        "is_chasing": m.is_chasing,
        "direction": int(m.direction),
    }


def monster_from_dict(d: dict) -> Monster:
    return Monster(
        base_stats=character_stats_from_dict(d["base_stats"]),
        type=MonsterType(d["type"]),
        hostility=HostilityLevel(d["hostility"]),
        is_chasing=d["is_chasing"],
        direction=Direction(d["direction"]),
    )


# === Баффы ===

def buff_to_dict(b: Buff) -> dict:
    return {"stat_increase": b.stat_increase, "effect_end": b.effect_end}


def buff_from_dict(d: dict) -> Buff:
    return Buff(stat_increase=d["stat_increase"], effect_end=d["effect_end"])


def active_buffs_to_dict(ab: ActiveBuffs) -> dict:
    return {
        "health_buffs": [buff_to_dict(b) for b in ab.health_buffs],
        "agility_buffs": [buff_to_dict(b) for b in ab.agility_buffs],
        "strength_buffs": [buff_to_dict(b) for b in ab.strength_buffs],
    }


def active_buffs_from_dict(d: dict) -> ActiveBuffs:
    return ActiveBuffs(
        health_buffs=[buff_from_dict(b) for b in d.get("health_buffs", [])],
        agility_buffs=[buff_from_dict(b) for b in d.get("agility_buffs", [])],
        strength_buffs=[buff_from_dict(b) for b in d.get("strength_buffs", [])],
    )


# === Рюкзак ===

def backpack_to_dict(bp: Backpack) -> dict:
    return {
        "foods": [food_to_dict(f) for f in bp.foods],
        "elixirs": [elixir_to_dict(e) for e in bp.elixirs],
        "scrolls": [scroll_to_dict(s) for s in bp.scrolls],
        "weapons": [weapon_to_dict(w) for w in bp.weapons],
        "treasures": treasure_to_dict(bp.treasures),
    }


def backpack_from_dict(d: dict) -> Backpack:
    return Backpack(
        foods=[food_from_dict(f) for f in d.get("foods", [])],
        elixirs=[elixir_from_dict(e) for e in d.get("elixirs", [])],
        scrolls=[scroll_from_dict(s) for s in d.get("scrolls", [])],
        weapons=[weapon_from_dict(w) for w in d.get("weapons", [])],
        treasures=treasure_from_dict(d.get("treasures", {"value": 0})),
    )


# === Игрок ===

def player_to_dict(p: Player) -> dict:
    return {
        "base_stats": character_stats_to_dict(p.base_stats),
        "max_health": p.max_health,
        "backpack": backpack_to_dict(p.backpack),
        "weapon": weapon_to_dict(p.weapon),
        "buffs": active_buffs_to_dict(p.buffs),
    }


def player_from_dict(d: dict) -> Player:
    return Player(
        base_stats=character_stats_from_dict(d["base_stats"]),
        max_health=d["max_health"],
        backpack=backpack_from_dict(d["backpack"]),
        weapon=weapon_from_dict(d["weapon"]),
        buffs=active_buffs_from_dict(d.get("buffs", {})),
    )


# === Комната ===

def room_to_dict(r: Room) -> dict:
    return {
        "coords": rect_to_dict(r.coords),
        "consumables": room_consumables_to_dict(r.consumables),
        "monsters": [monster_to_dict(m) for m in r.monsters],
    }


def room_from_dict(d: dict) -> Room:
    return Room(
        coords=rect_from_dict(d["coords"]),
        consumables=room_consumables_from_dict(d.get("consumables", {})),
        monsters=[monster_from_dict(m) for m in d.get("monsters", [])],
    )


# === Коридор ===

def passage_to_dict(p: Passage) -> dict:
    return {"pos": position_to_dict(p.pos), "size": size_to_dict(p.size)}


def passage_from_dict(d: dict) -> Passage:
    return Passage(
        pos=position_from_dict(d["pos"]),
        size=size_from_dict(d["size"]),
    )


# === Уровень ===

def level_to_dict(lv: Level) -> dict:
    return {
        "coords": rect_to_dict(lv.coords),
        "rooms": [room_to_dict(r) for r in lv.rooms],
        "passages": [passage_to_dict(p) for p in lv.passages],
        "level_num": lv.level_num,
        "exit_pos": rect_to_dict(lv.exit_pos),
    }


def level_from_dict(d: dict) -> Level:
    return Level(
        coords=rect_from_dict(d["coords"]),
        rooms=[room_from_dict(r) for r in d.get("rooms", [])],
        passages=[passage_from_dict(p) for p in d.get("passages", [])],
        level_num=d["level_num"],
        exit_pos=rect_from_dict(d["exit_pos"]),
    )


# === Информация о бое ===

def battle_info_to_dict(bi: BattleInfo) -> dict:
    return {
        "is_fight": bi.is_fight,
        "enemy": monster_to_dict(bi.enemy) if bi.enemy else None,
        "vampire_first_attack": bi.vampire_first_attack,
        "ogre_cooldown": bi.ogre_cooldown,
        "player_asleep": bi.player_asleep,
    }


def battle_info_from_dict(d: dict) -> BattleInfo:
    return BattleInfo(
        is_fight=d.get("is_fight", False),
        enemy=monster_from_dict(d["enemy"]) if d.get("enemy") else None,
        vampire_first_attack=d.get("vampire_first_attack", True),
        ogre_cooldown=d.get("ogre_cooldown", False),
        player_asleep=d.get("player_asleep", False),
    )


# === Видимость карты ===

def map_visibility_to_dict(mv: MapVisibility) -> dict:
    return {
        "visible_rooms": mv.visible_rooms,
        "visible_passages": mv.visible_passages,
    }


def map_visibility_from_dict(d: dict) -> MapVisibility:
    return MapVisibility(
        visible_rooms=d.get("visible_rooms", [False] * 9),
        visible_passages=d.get("visible_passages", []),
    )


# === Статистика сессии ===

def session_stats_to_dict(s: SessionStats) -> dict:
    return {
        "treasures": s.treasures,
        "level": s.level,
        "enemies_killed": s.enemies_killed,
        "food_eaten": s.food_eaten,
        "elixirs_drunk": s.elixirs_drunk,
        "scrolls_read": s.scrolls_read,
        "attacks_given": s.attacks_given,
        "hits_taken": s.hits_taken,
        "tiles_walked": s.tiles_walked,
    }


def session_stats_from_dict(d: dict) -> SessionStats:
    return SessionStats(
        treasures=d.get("treasures", 0),
        level=d.get("level", 0),
        enemies_killed=d.get("enemies_killed", 0),
        food_eaten=d.get("food_eaten", 0),
        elixirs_drunk=d.get("elixirs_drunk", 0),
        scrolls_read=d.get("scrolls_read", 0),
        attacks_given=d.get("attacks_given", 0),
        hits_taken=d.get("hits_taken", 0),
        tiles_walked=d.get("tiles_walked", 0),
    )


# === Полное состояние игры ===

def game_state_to_dict(gs: GameState) -> dict:
    return {
        "player": player_to_dict(gs.player),
        "level": level_to_dict(gs.level),
        "visibility": map_visibility_to_dict(gs.visibility),
        "battles": [battle_info_to_dict(b) for b in gs.battles],
        "stats": session_stats_to_dict(gs.stats),
    }


def game_state_from_dict(d: dict) -> GameState:
    return GameState(
        player=player_from_dict(d["player"]),
        level=level_from_dict(d["level"]),
        visibility=map_visibility_from_dict(d.get("visibility", {})),
        battles=[battle_info_from_dict(b) for b in d.get("battles", [])],
        stats=session_stats_from_dict(d.get("stats", {})),
    )
