"""Router. The library page holds the process knowledge; this file only frames it."""

import streamlit as st

from sic_ui import chip, inject_styles

st.set_page_config(page_title="碳化硅工艺知识库", page_icon="⚡", layout="wide")
inject_styles()

library = st.Page("pages/00_Process_Library.py", title="工艺知识库", default=True)
board = st.Page("pages/14_Process_Board.py", title="工艺看板")
synthesis = st.Page("pages/13_Synthesis.py", title="会议总结")
knowledge = st.Page("pages/01_Knowledge_Map.py", title="知识层")
sj = st.Page("pages/04_Superjunction.py", title="超结")
mos = st.Page("pages/03_MOS_Trench_FinFET.py", title="MOS 与沟槽")
defects = st.Page("pages/05_Defects_Bipolar.py", title="缺陷与双极")
tools = st.Page("pages/10_Engineering_Tools.py", title="工程工具")
jfet = st.Page("pages/09_SiC_JFET_Deep_Dive.py", title="JFET")
pack = st.Page("pages/02_ICSCRM_2026_Pack.py", title="周日教程")
reliability = st.Page("pages/06_Reliability_REDR.py", title="可靠性")
module = st.Page("pages/07_Module_WPT.py", title="模块")
infineon = st.Page("pages/08_Infineon_Devices.py", title="器件对照")
atlas = st.Page("pages/11_Abstract_Atlas.py", title="工艺数据库")
search = st.Page("pages/12_Semantic_Search.py", title="文献查阅")

page = st.navigation(
    {
        "知识库": [library, pack, board, synthesis, knowledge],
        "晶圆工艺": [sj, mos, defects, tools, jfet],
        "教程里的另一层": [reliability, module, infineon],
        "原文记录": [atlas, search],
    }
)

with st.sidebar:
    st.caption("周日下午的器件、退化和模块三讲单独放。晶圆制作顺序只收会议摘要里的工艺。")
    st.markdown(chip("PDF 留在本机"))
    st.caption("🟢 教程原文 · 🔵 推导 · 🟠 工程模型 · 🟣 会议摘要")

page.run()
