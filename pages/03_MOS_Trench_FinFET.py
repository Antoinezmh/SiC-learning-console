import streamlit as st

from diagrams import mobility_split, trench_corner
from sic_ui import hero, inject_styles, section

inject_styles()
hero(
    "MOS interface",
    "平面、沟槽和 Fin",
    "沟道电阻看有多少电子是自由的。沟槽把这个界面放到侧壁上，同时把氧化层电场赶到拐角。",
)

section("自由电荷和被陷电荷", "Split C–V + MOS-Hall")
left, right = st.columns([1, 1.15])
with left:
    st.latex(r"\mu_{ch}\approx\mu_{free}\frac{n_{free}}{n_{free}+n_{trap}}")
    st.markdown(
        "教程用 Split C–V 和 MOS-Hall 把自由电荷、被陷电荷分开。"
        "迁移率公式是教学模型：被陷的那一份不参与导电。🟠"
    )
    trapped = st.slider("被陷比例 n_trap / (n_free+n_trap)", 0.0, 0.9, 0.55, 0.05)
with right:
    st.plotly_chart(mobility_split(trapped), width="stretch")

section("导通电阻拆开", "哪一项还值得做")
st.latex(r"R_{on}=R_{ch}+R_{acc}+R_{JFET}+R_{drift}+R_{sub}+R_{contact}")
st.markdown(
    "沟道迁移率变好，只降低 R_ch。1200 V 附近要问它在总电阻里还占多少；"
    "电压再高，漂移区通常更大。175–200°C 还要问哪一项随温度升得最快。"
)

section("沟槽角", "几何，不只是界面态")
c1, c2 = st.columns([1.1, 1])
with c1:
    st.plotly_chart(trench_corner(), width="stretch")
with c2:
    st.markdown(
        "红点是底部拐角。尖角把氧化层电场抬高，栅漏电和经时击穿先从这里开始。"
    )
    st.markdown(
        "本次会议 Tu-3A-02：高温退火让表面原子迁移、把角抹圆。"
        "Ar 退火顶角半径约 **138 nm**，H₂ 退火约 **80 nm**。"
        "两者都压低了 V_GS = 22 V 下的 I_GSS，并收紧了片内离散。CDE 能修一点角，但会改沟槽角度。🟣"
    )
    st.markdown(
        "侧壁晶面决定输运。屏蔽结构能把氧化层电场拉下来，同时往往加长或收窄电流路径，R_on 会回去一部分。"
    )
    st.caption("截面是示意，半径数字来自该篇摘要正文，不是这张图的测量坐标。")

section("Fin")
st.markdown(
    "Fin 用来看静电势、陷落和迁移率怎么随宽度变。"
    "具体性能数字要回到原始论文，不从这张教学图外推。🟣"
)
