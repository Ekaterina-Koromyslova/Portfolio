from __future__ import annotations

import json
import os

from interfaces.data_interfaces import IDataService
from dto.entities import GameState, SessionStats
from datalayer.serializers import (
    game_state_to_dict, game_state_from_dict,
    session_stats_to_dict, session_stats_from_dict,
)

DEFAULT_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


class JsonDataService(IDataService):

    def __init__(self, data_dir: str = DEFAULT_DATA_DIR) -> None:
        self._data_dir = data_dir
        os.makedirs(self._data_dir, exist_ok=True)
        self._save_path = os.path.join(self._data_dir, "save.json")
        self._stats_path = os.path.join(self._data_dir, "statistics.json")
        self._score_path = os.path.join(self._data_dir, "scoreboard.json")

        if not os.path.exists(self._score_path):
            self._write_json(self._score_path, {"sessions": []})

    def save_game(self, state: GameState) -> None:
        self._write_json(self._save_path, game_state_to_dict(state))

    def load_game(self) -> GameState | None:
        data = self._read_json(self._save_path)
        if data is None:
            return None
        try:
            return game_state_from_dict(data)
        except (KeyError, TypeError, ValueError):
            return None

    def has_save(self) -> bool:
        return os.path.isfile(self._save_path)

    def reset_save(self) -> None:
        if os.path.isfile(self._save_path):
            os.remove(self._save_path)

    def save_session_stats(self, stats: SessionStats) -> None:
        self._write_json(self._stats_path, session_stats_to_dict(stats))

    def load_session_stats(self) -> SessionStats:
        data = self._read_json(self._stats_path)
        if data is None:
            return SessionStats()
        return session_stats_from_dict(data)

    def finalize_session(self, stats: SessionStats) -> None:
        data = self._read_json(self._score_path)
        if data is None:
            data = {"sessions": []}
        data["sessions"].append(session_stats_to_dict(stats))
        self._write_json(self._score_path, data)

    def load_leaderboard(self) -> list[SessionStats]:
        data = self._read_json(self._score_path)
        if data is None:
            return []
        entries = [
            session_stats_from_dict(s)
            for s in data.get("sessions", [])
        ]
        entries.sort(key=lambda s: s.treasures, reverse=True)
        return entries

    @staticmethod
    def _write_json(path: str, data: dict) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def _read_json(path: str) -> dict | None:
        if not os.path.isfile(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return None
