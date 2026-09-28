import streamlit as st

from diagrams import ionization_anchor, sj_cross_section, sj_field
from sic_ui import hero, inject_styles, section

inject_styles()
hero(
    "Device physics",
    "碳化硅超结",
    "交替 P/N 柱把漂移区电场从三角形拉平，同样耐压下可以更重掺杂、更低比导通电阻。图是示意，不是 TCAD。",
)

section("电荷平衡", "Q_N ≈ Q_P")
c1, c2 = st.columns(2)
with c1:
    st.plotly_chart(sj_cross_section(), width="stretch")
    st.latex(r"Q_N=q N_D W_N \qquad Q_P=q N_A^- W_P")
with c2:
    imb = st.slider("示意电荷失衡 ΔQ (%)", -40, 40, 0, 5)
    st.plotly_chart(sj_field(imb), width="stretch")
    st.caption("橙色是教学用的平坦场参考。失衡越大，电场越向柱的一端倾斜，先碰到临界场的是峰值而不是平均值。🟠")

section("p 型柱的有效电荷", "Al 不完全电离")
st.markdown(
    "4H-SiC 里铝替硅位，六方和立方位的电离能大约是 **197.9 meV** 和 **201.3 meV**。"
    "中性区在室温不会全部电离，所以电荷平衡要用电离后的 N_A⁻，不能只用注入剂量。"
)
st.plotly_chart(ionization_anchor(), width="stretch")
st.caption(
    "两个点来自同一则公开计算例子：掺杂 1×10¹⁷ cm⁻³、电离能取 200 meV 时，室温大约电离 15%，300°C 大约 75%。"
    "这不是本会议的测量，也没有把中间温度插成器件模型。"
    "另有 MeV 铝注入做超结柱的 Hall 结果，有效电离能大约 330 meV，高于通常说的 200 meV。"
    "所以室温配平的柱，到 175–200°C 是否还配平，要单独问。🟠"
)

section("两条造柱路线", "扩散几乎帮不上忙")
st.markdown(
    "4H-SiC 里掺杂几乎不扩散，硅超结那种多次浅注入再推进的办法走不通。"
    "柱深要么靠高能或沟道注入，要么靠沟槽再外延填回去。"
)
a, b = st.columns(2)
with a:
    st.markdown("**沟道注入 · 单次或少次外延**")
    st.markdown(
        "- 本次会议 Fr-1B-02：1200 V 柱深约 5–8 μm，掺杂约 1×10¹⁶–1×10¹⁷ cm⁻³；Al 到约 12 MeV，P 到约 14 MeV，沿 [0001]。🟣\n"
        "- 公开器件：沟道注入两步外延，柱约 4.9 μm、击穿约 1000 V；常规高能注入三步，柱约 3.7 μm、击穿约 800 V；大约 210 V/μm。来源是 Materials Science Forum 1062 (2022) 549。"
    )
with b:
    st.markdown("**沟槽外延填充**")
    st.markdown(
        "- 本次会议 We-3B-02：SiH₄:C₃H₈:H₂ + TMA，加 HCl；填充到约 10 μm/h，沟槽深到约 50 μm。部分超结 MOSFET 约 7.8 kV、17.8 mΩ·cm²，柱深约 25 μm。Al 在 (0001) 比侧壁掺得多。🟣\n"
        "- 公开工艺：1550°C、HSiCl₃ + HCl，3 μm 宽沟槽填充速率 19±0.4 μm/h；侧壁角度和 HCl 流量决定会不会封出空洞。Warwick 仓库稿 191216。"
    )
st.caption("左列的会议数字和右列以外的论文数字不要画在同一条标定曲线上。它们回答的是同一类工艺问题，实验条件并不相同。")

section("会议工艺还没写完的")
st.markdown(
    "柱再变深时，沟道注入的能量和损伤、沟槽填充的形貌和掺杂均匀性，要各自留在对应摘要里。"
    "终端要和柱的电场整形同时成立。"
)
st.caption("约 10 kV 及以上更值得看 IGBT，是周日 Harada 教程里的器件范围，不是这条造柱工艺的结论。")
