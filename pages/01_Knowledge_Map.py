import streamlit as st

from diagrams import knowledge_stack
from sic_ui import hero, inject_styles, section

inject_styles()
hero(
    "Map",
    "知识层",
    "从晶体到系统，每一层记下自己留下的结构。晶圆制作顺序只使用其中的晶体、外延、工艺和界面。模块和系统属于周日教程的后半段，不并进那条顺序。",
)

left, right = st.columns([1.05, 1])
with left:
    st.plotly_chart(knowledge_stack(), width="stretch")
with right:
    section("每一层留下什么")
    notes = [
        ("材料", "4H 多型、临界场大约比硅高一个量级、各向异性。"),
        ("晶体 / 外延", "PVT 长晶，台阶流外延，掺杂和宏观缺陷。"),
        ("缺陷", "V_C / Z1/2，BPD，TED/TSD，层错。"),
        ("工艺", "注入、氧化、退火、沟槽、超结柱。掺杂几乎不扩散。"),
        ("MOS 界面", "自由电荷和被陷电荷，侧壁晶面。"),
        ("器件", "SBD、平面/沟槽 MOSFET、JFET、超结、IGBT。"),
        ("可靠性", "BTI、栅氧、双极退化、短路和雪崩。"),
        ("模块", "热、键合、寄生电感、栅驱。"),
        ("系统", "变换器、保护、效率和功率密度。"),
    ]
    for name, text in notes:
        st.markdown(f"**{name}** · {text}")

section("一条跨层链", "BPD")
st.markdown(
    "衬底 BPD → 少数载流子复合 → 基面层错扩张 → 寿命和通态退化 → 体二极管能不能用、要不要加复合缓冲层。"
    "这是教程推导出来的用法，机制本身在公开文献里是复合增强位错滑移。🔵"
)
