"""Cross-checked SiC gate-process conditions for channel mobility."""

from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from sic_ui import badge, hero, inject_styles, section

ROOT = Path(__file__).resolve().parents[1]
BOARD = json.loads((ROOT / "data" / "process_board.json").read_text(encoding="utf-8"))

STATUS = {
    "cross": ("ok", "交叉"),
    "group": ("info", "同组复现"),
    "single": ("yellow", "单篇"),
    "conflict": ("yellow", "温度未合成"),
    "avoid": ("gray", "另一道工序"),
}
MARK = {
    "pass": ("ok", "过线"),
    "fail": ("gray", "未过"),
    "note": ("yellow", "测法不同"),
}

inject_styles()
hero(
    "Process board",
    "工艺看板",
    BOARD["goal"],
)

section("判定标准", "pass / fail")
metric_cols = st.columns(4)
for col, rule in zip(metric_cols, BOARD["criteria"]):
    with col:
        with st.container(border=True):
            st.markdown(f"**{rule['metric']}**")
            st.markdown(rule["pass_line"])
            st.caption(rule["method"])

for rule in BOARD["criteria"]:
    with st.expander(f"{rule['metric']} 的线和容易误判的地方"):
        st.markdown(rule["evidence"])
        st.markdown(rule["trap"])
        st.caption("　".join(f"[{pid}](/Abstract_Atlas?paper={pid})" for pid in {
            "dit": ["Mo-1A-01", "Mo-1A-02", "Mo-1A-03", "Mo-P-90LN"],
            "mu": ["Mo-1A-01", "Mo-1A-03", "We-P-33"],
            "vth": ["Mo-1A-01", "We-P-33", "Fr-3A-04"],
            "joint": ["Mo-1A-01", "Mo-1A-03"],
        }[rule["id"]]))

section("按这条标准看谁最优", "one goal")
goal_labels = {item["id"]: item["title"] for item in BOARD["goals"]}
goal_id = st.radio(
    "判定目标",
    list(goal_labels),
    format_func=lambda key: goal_labels[key],
    horizontal=True,
    label_visibility="collapsed",
)
goal = next(item for item in BOARD["goals"] if item["id"] == goal_id)
for call in goal["calls"]:
    level, label = MARK[call["mark"]]
    with st.container(border=True):
        st.markdown(badge(level, label) + f"  **{call['name']}**", unsafe_allow_html=True)
        st.markdown(call["detail"])
        st.caption("　".join(f"[{pid}](/Abstract_Atlas?paper={pid})" for pid in call["papers"]))

section("两条可以分开走的栅流程", "by criterion")
route_cols = st.columns(2)
for col, route in zip(route_cols, BOARD["routes"]):
    level, label = STATUS[route["status"]]
    with col:
        with st.container(border=True):
            st.markdown(badge(level, label) + f"  **{route['title']}**", unsafe_allow_html=True)
            st.markdown(route["steps"])
            st.markdown(route["why"])
            st.caption(route["limit"])

section("关键流程", "gate stack")
for start in (0, 4):
    flow_cols = st.columns(4)
    for col, step in zip(flow_cols, BOARD["flow"][start : start + 4]):
        level, label = STATUS[step["status"]]
        with col:
            with st.container(border=True):
                st.caption(f"{step['n']}  {label}")
                st.markdown(f"**{step['name']}**")
                st.markdown(step["choice"])

section("选择一种条件", "cross-check")
labels = {item["id"]: item["title"] for item in BOARD["conditions"]}
picked = st.radio(
    "工艺条件",
    list(labels),
    format_func=lambda key: labels[key],
    horizontal=True,
    label_visibility="collapsed",
)
item = next(row for row in BOARD["conditions"] if row["id"] == picked)
level, label = STATUS[item["status"]]
st.markdown(badge(level, label) + f"  **{item['title']}**", unsafe_allow_html=True)
st.caption(item["kicker"])
st.markdown(item["verdict"])

for row in item["rows"]:
    with st.container(border=True):
        st.markdown(f"**{row['condition']}**")
        st.markdown(row["result"])
        links = "　".join(f"[{pid}](/Abstract_Atlas?paper={pid})" for pid in row["papers"])
        st.caption(f"{row['tag']}  ·  {links}")

section("机理", item["title"])
st.markdown(item["mechanism"])
st.markdown(
    "散射分成三项：库仑（界面电荷）、声子、表面粗糙。"
    "温度升高迁移率还在升，说明库仑项仍占着；Fin 收到约 200 nm 以下，温度系数变负，声子项才露出来（We-2A-06LN）。"
    "NO 和氢预退火动的是库仑项。沟槽圆角动的是氧化层电场。"
)
