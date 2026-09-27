import streamlit as st
import plotly.graph_objects as go

st.title("📡 SJ Risk Radar")
st.caption("风险雷达用于组织讨论，不把不同论文的性能数据伪装成统一评分。")
route=st.selectbox("Route",["Channeling","MeV implantation","Multi-epi","TFE"])
profiles={
"Channeling":[4,2,4,3,3,2],
"MeV implantation":[3,3,4,2,3,3],
"Multi-epi":[2,4,2,4,2,4],
"TFE":[4,3,3,4,5,3]}
labels=["Cycle-time pressure","Alignment sensitivity","Implant damage","Repeated modules","Void/fill risk","Tool specialization"]
vals=profiles[route]
fig=go.Figure(go.Scatterpolar(r=vals+[vals[0]],theta=labels+[labels[0]],fill="toself"))
fig.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,5])))
st.plotly_chart(fig,use_container_width=True)
st.warning("🟠 Qualitative discussion aid. Scores are not source-direct measurements and must not be used as a vendor/fab qualification score.")
st.markdown("**Use the radar to ask what must be characterized next—not to declare a winner.**")
