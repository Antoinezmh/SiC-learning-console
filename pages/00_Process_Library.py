"""Long-term SiC process library: sequence, relations, and how a flow is specified."""

from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from sic_ui import badge, hero, inject_styles, page_link, section
from sicdb import load_cards, load_catalog, load_signals

ROOT = Path(__file__).resolve().parents[1]
LIB = json.loads((ROOT / "data" / "process_library.json").read_text(encoding="utf-8"))
TUTORIAL = json.loads((ROOT / "data" / "tutorial_sunday.json").read_text(encoding="utf-8"))

KIND = {
    "使能": "ok",
    "传递": "info",
    "决定": "info",
    "分开": "yellow",
    "冲突": "gray",
}
RECORD_PAGE = {
    "Synthesis": "13_Synthesis.py",
    "Superjunction": "04_Superjunction.py",
    "MOS_Trench_FinFET": "03_MOS_Trench_FinFET.py",
    "Process_Board": "14_Process_Board.py",
    "Defects_Bipolar": "05_Defects_Bipolar.py",
}

inject_styles()
catalog = load_catalog()
signals = load_signals()
cards = load_cards()

hero(
    "SiC process library",
    "碳化硅工艺知识库",
    "周日教程和晶圆工艺分成两份记录。下面的制作顺序只收会议摘要里的工艺条件和步骤关系。下午三讲不进入这条顺序。",
    meta_html=(
        f"<b>{len(catalog)}</b> 篇摘要 · "
        f"<b>{len(signals)}</b> 条正文参数 · "
        f"<b>{len(cards)}</b> 张核对工艺卡 · "
        f"<b>{len(LIB['relations'])}</b> 条工艺关系"
    ),
)

section("周日下午的三讲", "kept apart")
st.markdown(
    "9 月 27 日教程后半段是下一代器件、材料退化和功率模块。"
    "三讲留在教程记录里，不作为下面晶圆制作顺序的一步，也不提供栅氧合格线。"
)
cols = st.columns(3)
for col, talk in zip(cols, TUTORIAL["afternoon"]):
    with col:
        with st.container(border=True):
            st.markdown(f"**{talk['who']}**")
            st.markdown(talk["title"])
            st.caption(talk["scope"])
page_link("pages/02_ICSCRM_2026_Pack.py", "打开周日教程", icon=":material/arrow_forward:")

section("晶圆工艺", "abstract record")
labels = {step["id"]: step["name"] for step in LIB["spine"]}
picked = st.radio(
    "工序",
    list(labels),
    format_func=lambda key: labels[key],
    horizontal=True,
    label_visibility="collapsed",
)
step = next(item for item in LIB["spine"] if item["id"] == picked)
with st.container(border=True):
    st.markdown(f"**这一步定下来的是** {step['locks']}")
    st.markdown(step["make"])
    st.caption(f"交给下一步 · {step['feeds']}")
    page_link(f"pages/{RECORD_PAGE[step['record']]}", "打开对应记录", icon=":material/arrow_forward:")

section("和其他工序的关系", step["name"])
related = [row for row in LIB["relations"] if step["id"] in row["steps"]]
if not related:
    st.caption("这一步的关系写在相邻工序上。")
for row in related:
    with st.container(border=True):
        st.markdown(
            badge(KIND[row["kind"]], row["kind"])
            + f"  **{row['left']}** → **{row['right']}**",
            unsafe_allow_html=True,
        )
        st.markdown(row["text"])
        st.caption("　".join(f"[{pid}](/Abstract_Atlas?paper={pid})" for pid in row["papers"]))

section("全部关系", "kept as records")
for row in LIB["relations"]:
    st.markdown(
        badge(KIND[row["kind"]], row["kind"])
        + f"  {row['left']} → {row['right']}",
        unsafe_allow_html=True,
    )

section("怎样把一套工艺做合格", "design sequence")
for item in LIB["design"]:
    with st.container(border=True):
        st.markdown(f"**{item['n']}  {item['name']}**")
        st.markdown(item["text"])

section("记录入口", "same library")
links = [
    ("工艺看板", "栅条件的合格线和对照", "pages/14_Process_Board.py"),
    ("会议总结", "外延、体单晶、沟槽、超结的模块记录", "pages/13_Synthesis.py"),
    ("工艺数据库", "按温度、能量、掺杂、气氛查看正文参数", "pages/11_Abstract_Atlas.py"),
    ("知识层", "从晶体到系统，每一层交给下一层什么", "pages/01_Knowledge_Map.py"),
]
cols = st.columns(2)
for col, (name, desc, path) in zip(cols, links[:2]):
    with col:
        with st.container(border=True):
            st.markdown(f"**{name}**")
            st.caption(desc)
            page_link(path, f"打开{name}", icon=":material/arrow_forward:")
cols = st.columns(2)
for col, (name, desc, path) in zip(cols, links[2:]):
    with col:
        with st.container(border=True):
            st.markdown(f"**{name}**")
            st.caption(desc)
            page_link(path, f"打开{name}", icon=":material/arrow_forward:")
