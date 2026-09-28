import streamlit as st

from diagrams import bpd_schematic, lifetime_bars
from sic_ui import hero, inject_styles, section

inject_styles()
hero(
    "Defects",
    "基面位错和双极退化",
    "少数载流子在基面位错上复合，会驱动单肖克莱层错沿基面扩张，通态压降跟着变。",
)

section("两条路径", "转换，或挡住空穴")
mode = st.radio("看哪一种", ["外延把 BPD 转成 TED", "空穴到达衬底，层错扩张"], horizontal=True)
st.plotly_chart(
    bpd_schematic("convert" if mode.startswith("外延") else "expand"),
    width="stretch",
)
if mode.startswith("外延"):
    st.markdown(
        "BPD 和 TED 可以有同一个伯格斯矢量，所以外延一开始就能在衬底界面附近把 BPD 折成垂直的 TED。"
        "TED 沿 c 轴，不在基面上滑。公开外延工作里，把生长速率从 5 μm/h 提到 24 μm/h（4° 偏角）后，"
        "外延层 BPD 可以低到 0.1 cm⁻² 量级，用来做约 1 cm² 的器件。来源是 ECS Meeting Abstract MA2022-01 1135。"
    )
else:
    st.markdown(
        "漂移区里剩下的 BPD，或者缓冲层里还没转完的那段，在双极注入下仍会扩成层错。"
        "高掺 n+ 缓冲提高复合、减少到达衬底的空穴，是教程里的办法。🟢"
        "质子注入是另一条公开路线，用来压住 1SSF 扩张（Scientific Reports, 2022, s41598-022-23691-y）。"
    )
st.caption("图是截面示意。4° 偏角和层错的真实几何没有按比例画。")

section("碳空位和寿命", "Z1/2")
st.plotly_chart(lifetime_bars(), width="stretch")
st.caption(
    "教程给出的一组例子：大约 1.8 μs，消除空位后到 28.1 μs，表面钝化后再到 34.2 μs。"
    "Z1/2 对应碳空位 V_C。🟢 这是一条样品上的变化，不是产线规格。"
)
