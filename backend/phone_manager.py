"""Phone management logic backed by data/phones.json.

This module exposes simple helpers used by the UI to list, add,
find and delete phone records persisted in `data/phones.json`.
"""

import json
import os
from typing import List, Optional

DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "phones.json"))


def _load_all() -> List[dict]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
        except json.JSONDecodeError:
            return []


def _save_all(phones: List[dict]) -> None:
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(phones, f, indent=2, ensure_ascii=False)


def list_phones() -> List[dict]:
    """Return all phones from the JSON store."""
    return _load_all()


def add_phone(phone_data: dict) -> None:
    phones = _load_all()
    phones.append(phone_data)
    _save_all(phones)


def find_phone_by_id(phone_id) -> Optional[dict]:
    phones = _load_all()
    for p in phones:
        if p.get("id") == phone_id:
            return p
    return None


def delete_phone(phone_id) -> None:
    """Delete a phone from the JSON store by id.

    Raises ValueError if the phone is not found.
    """
    phones = _load_all()
    for idx, p in enumerate(phones):
        if p.get("id") == phone_id:
            phones.pop(idx)
            _save_all(phones)
            return
    raise ValueError(f"Phone with id {phone_id} not found")
