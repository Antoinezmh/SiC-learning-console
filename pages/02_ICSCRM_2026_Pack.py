"""Sunday 27 Sep 2026 tutorial, kept as lectures rather than wafer-process steps."""

from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from sic_ui import badge, hero, inject_styles, section

ROOT = Path(__file__).resolve().parents[1]
DAY = json.loads((ROOT / "data" / "tutorial_sunday.json").read_text(encoding="utf-8"))

inject_styles()
hero(
    "27 Sep 2026",
    "周日教程",
    DAY["note"],
    meta_html=DAY["place"],
)

section("上午", "fundamentals and systems")
for talk in DAY["morning"]:
    with st.container(border=True):
        st.markdown(badge("ok", "🟢 教程") + f"  **{talk['who']} · {talk['title']}**", unsafe_allow_html=True)
        st.markdown(talk["scope"])
        st.markdown(talk["holds"])
        st.caption(talk["boundary"])

section("下午", "devices, degradation, modules")
st.caption("后半段三讲各自成篇。器件结构、退化机理、模块回路，不并进当前的晶圆工艺合格线。")
for talk in DAY["afternoon"]:
    with st.container(border=True):
        st.markdown(badge("info", "讲座范围") + f"  **{talk['who']} · {talk['title']}**", unsafe_allow_html=True)
        st.markdown(talk["scope"])
        st.markdown(talk["holds"])
        st.caption(talk["boundary"])
