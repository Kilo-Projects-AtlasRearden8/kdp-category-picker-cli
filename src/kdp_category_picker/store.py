"""Local picks store and KDP export (JSON file, no accounts, no keys)."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List, Optional

from .categories import Category


@dataclass
class Pick:
    category_id: str
    category_path: str
    note: str = ""


@dataclass
class PicksStore:
    path: Path
    picks: List[Pick] = field(default_factory=list)

    @classmethod
    def load(cls, path: Path) -> "PicksStore":
        picks: List[Pick] = []
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                for item in data.get("picks", []):
                    picks.append(
                        Pick(
                            category_id=item.get("category_id", ""),
                            category_path=item.get("category_path", ""),
                            note=item.get("note", ""),
                        )
                    )
            except (json.JSONDecodeError, OSError):
                picks = []
        return cls(path=path, picks=picks)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = {"picks": [asdict(p) for p in self.picks]}
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def add(self, category: Category, note: str = "") -> bool:
        for p in self.picks:
            if p.category_id == category.id:
                return False  # already saved
        self.picks.append(Pick(category_id=category.id, category_path=category.path, note=note))
        self.save()
        return True

    def remove(self, category_id: str) -> bool:
        before = len(self.picks)
        self.picks = [p for p in self.picks if p.category_id != category_id]
        if len(self.picks) < before:
            self.save()
            return True
        return False

    def list(self) -> List[Pick]:
        return list(self.picks)

    def clear(self) -> None:
        self.picks = []
        self.save()

    def export_csv(self, path: Path) -> None:
        """Export picks as a simple CSV for KDP upload."""
        path = Path(path)
        lines = ["Category Path,Category ID,Note"]
        for p in self.picks:
            # CSV-escape fields that may contain commas.
            def esc(s: str) -> str:
                s = s.replace('"', '""')
                return f'"{s}"' if "," in s or '"' in s or "\n" in s else s

            lines.append(f"{esc(p.category_path)},{esc(p.category_id)},{esc(p.note)}")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")


DEFAULT_STORE_PATH = Path.home() / ".kdp_category_picker" / "picks.json"


def get_store(path: Optional[Path] = None) -> PicksStore:
    return PicksStore.load(path or DEFAULT_STORE_PATH)
