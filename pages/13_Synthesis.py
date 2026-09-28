"""Module-level reading of the ICSCRM 2026 abstract book."""

from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from sic_ui import hero, inject_styles, section
from sicdb import MODULE_LABEL, load_catalog

ROOT = Path(__file__).resolve().parents[1]
SUMMARIES = json.loads((ROOT / "data" / "summaries.json").read_text(encoding="utf-8"))

inject_styles()
catalog = load_catalog()
primary: dict[str, int] = {}
for row in catalog:
    key = row.get("primary_module") or "other"
    primary[key] = primary.get(key, 0) + 1

hero(
    "ICSCRM 2026",
    "会议总结",
    "按外延、体单晶、栅堆叠、沟槽、超结和缺陷，把摘要正文里反复出现的工艺结论收在一起。每句都能点回编号。这些是会上的陈述，不是本机新测的数据。",
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("议程", len(catalog))
c2.metric("外延", primary.get("epi", 0))
c3.metric("超结", primary.get("sj", 0))
c4.metric("栅堆叠", primary.get("gate_stack", 0))
st.caption("题名归类只用于看出分量。总结里的数字来自摘要正文，图和表里没写成句子的数没有补进去。")

labels = {
    "overview": "总览",
    "epi": "外延",
    "bulk": "体单晶",
    "gate_stack": "栅堆叠",
    "trench": "沟槽",
    "sj": "超结",
    "defect": "缺陷",
    "open": "不要并在一起",
}

for block in SUMMARIES:
    module = block.get("module") or ""
    note = labels.get(module, "")
    if module in MODULE_LABEL:
        note = f"{MODULE_LABEL[module]} · {primary.get(module, 0)} 篇"
    section(block["title"], note)
    st.markdown(block["lead"])
    for point in block.get("points") or []:
        with st.container(border=True):
            st.markdown(point["text"])
            papers = point.get("papers") or []
            if papers:
                st.markdown("　".join(
                    f"[{pid}](/Abstract_Atlas?paper={pid})" for pid in papers
                ))
