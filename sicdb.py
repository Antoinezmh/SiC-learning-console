"""Load the ICSCRM catalog and process cards."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CATALOG = ROOT / "data" / "catalog.jsonl"
CARDS = ROOT / "data" / "process_cards.jsonl"
FACTS = ROOT / "data" / "paper_facts.jsonl"
SIGNALS = ROOT / "data" / "signals.jsonl"
ABSTRACTS = ROOT / "data" / "abstracts.jsonl"

KIND_LABEL = {
    "temperature": "温度",
    "energy": "注入能量",
    "dose": "注入剂量",
    "doping": "掺杂浓度",
    "length": "长度 / 深度",
    "growth_rate": "生长速率",
    "pressure": "压力",
    "wafer": "晶圆尺寸",
    "breakdown": "阻断电压",
    "ron": "比导通电阻",
    "fraction": "百分比",
}

MODULE_LABEL = {
    "bulk": "体单晶 / 晶圆",
    "epi": "外延",
    "implant": "注入",
    "trench": "沟槽",
    "sj": "超结",
    "gate_stack": "栅堆叠",
    "contact": "接触",
    "defect": "缺陷",
    "reliability": "可靠性",
    "device": "器件",
    "quantum": "量子",
    "other": "其他",
}


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def load_catalog() -> list[dict]:
    return _read_jsonl(CATALOG)


def load_cards() -> list[dict]:
    return _read_jsonl(CARDS)


def load_facts() -> list[dict]:
    return _read_jsonl(FACTS)


def load_signals() -> list[dict]:
    return _read_jsonl(SIGNALS)


def load_abstracts() -> dict[str, dict]:
    return {row["id"]: row for row in _read_jsonl(ABSTRACTS)}
