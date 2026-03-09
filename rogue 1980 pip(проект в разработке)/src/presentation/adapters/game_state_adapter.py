"""
Адаптер между domain и presentation.

Преобразует domain-сущности в простой view_state для UI
"""

from __future__ import annotations

from src.domain.entities.entities import (
    Player,
    Level,
    Room,
    Passage,
    BattleInfo,
    MapVisibility,   
)
