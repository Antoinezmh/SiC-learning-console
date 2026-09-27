import streamlit as st
from utils.principle_ui import causal_chain,takeaway

st.title("🧭 SJ Visual Learning Path")
st.caption("适合快速阅读、会议复习和给团队解释：每层只回答一个问题。")

steps=[
("① Why","为什么需要 SJ？","高压 MOSFET 的漂移区越来越厚、越来越轻掺杂，Rdrift 快速上升。"),
("② Physics","SJ 做了什么？","P/N 柱横向耗尽 → 电荷补偿 → 纵向电场更均匀 → N 柱允许更高掺杂。"),
("③ Structure","哪些结构？","Short-SJ / Semi-SJ / Full-SJ；结构深度与工艺难度共同增加。"),
("④ Process","怎么制造？","Multi-epi / TFE / MeV implant / Channeling，各自在深度、节拍、缺陷和均匀性上权衡。"),
("⑤ Dynamic","为什么静态最优还不够？","Incomplete ionization 会让开关瞬间的有效 QP 与静态值不同。"),
("⑥ Ruggedness","为什么 SC / Avalanche 会变化？","电场重新分布改变 J·E 热源位置，也改变雪崩与寄生效应的空间分布。"),
("⑦ Product","最后看什么？","不是单颗 best die，而是 wafer/lot/process window/yield/temperature/lifetime 下仍能成立。")
]
for title,q,a in steps:
    with st.expander(f"{title} · {q}",expanded=title.startswith("①")):
        st.write(a)

st.subheader("One-screen mental model")
causal_chain(["Voltage ↑","Rdrift ↑","SJ charge compensation","higher ND","Ron ↓","process sensitivity ↑","need process-window design"])
takeaway("学习 SJ 时始终沿着“为什么 → 物理 → 结构 → 工艺 → 动态 → 可靠性 → 产品化”走，不容易被单个漂亮指标带偏。")

st.subheader("Three questions after every figure")
st.markdown("""
1. **这张图改变了哪个物理量？** E-field、charge、lifetime、temperature 还是 current path？
2. **它改善了哪个器件指标？** Ron、BV、Qrr、SC、avalanche 还是 reliability？
3. **它付出了什么制造代价？** depth、alignment、damage、activation、uniformity、cycle time 还是 yield？
""")
