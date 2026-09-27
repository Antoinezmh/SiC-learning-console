import streamlit as st
import numpy as np
import plotly.graph_objects as go
from utils.content_loader import load_yaml

st.title("🏗️ SiC Superjunction — Design Workbench")
kb = load_yaml("content/tutorials/icscrm2026_superjunction.yaml")
st.caption("Source-aware workbench: tutorial facts are separated from engineering models and pending verification.")

st.subheader("1 · Charge balance")
c1,c2=st.columns(2)
with c1:
    nd=st.number_input("N-column doping ND (cm⁻³)",1e15,1e18,5e16,format="%.2e")
    wn=st.number_input("N-column width WN (μm)",0.1,20.0,2.0)
with c2:
    na=st.number_input("Nominal P-column doping NA (cm⁻³)",1e15,1e19,5e16,format="%.2e")
    wp=st.number_input("P-column width WP (μm)",0.1,20.0,2.0)
    ion=st.slider("Illustrative acceptor ionization fraction",0.10,1.00,0.70,0.01)

qn=nd*wn
qp=na*ion*wp
ratio=qp/qn
imb=(qn-qp)/qn
m1,m2=st.columns(2)
m1.metric("QP / QN",f"{ratio:.3f}")
m2.metric("ΔQ / QN",f"{imb*100:.2f} %")
st.caption("🟠 Engineering teaching model. Ionization fraction is user-specified; this app does not claim a calibrated temperature-dependent Al ionization model.")

x=np.linspace(0.8,1.2,161)
fig=go.Figure()
fig.add_trace(go.Scatter(x=x,y=np.abs(1-x)*100,name="|charge imbalance|"))
fig.add_vline(x=1.0,line_dash="dash")
fig.update_layout(xaxis_title="QP / QN",yaxis_title="|ΔQ| / QN (%)",title="Charge-balance sensitivity coordinate")
st.plotly_chart(fig,use_container_width=True)

st.subheader("2 · Process routes")
st.dataframe({
 "Route":["Multi-epi","High-energy implantation","Channeling implantation","Trench filling / epi fill"],
 "Core idea":["Repeated epi + selective doping","Deep implanted P region","Use crystal channeling for deeper implant","Deep trench followed by filling"],
 "Current evidence":["Pending source extraction","Tutorial discusses implantation route","Tutorial: process-cycle-time advantage","Tutorial: more attractive for deeper columns"],
 "Status":["🟣 Verify","🔵/🟣 Verify details","🟢 Tutorial direct","🟢 Tutorial direct"]
},hide_index=True,use_container_width=True)

st.subheader("3 · Productization matrix")
st.dataframe({
 "Layer":["Physics","Static","Dynamic","Ruggedness","Process","Manufacturing"],
 "Questions":["Charge balance / incomplete ionization","BV, Ron,sp, Ron(T)","Qrr, Coss/Crss, transient field","SC, avalanche, forward current","depth, activation, fill/implant damage","uniformity, window, yield, cycle time"]
},hide_index=True,use_container_width=True)

st.subheader("4 · Temperature / ionization experiment")
temps=np.array([25,75,125,175,200])
f25=st.slider("Illustrative ionization fraction @25°C",0.1,1.0,0.55,0.01)
f200=st.slider("Illustrative ionization fraction @200°C",0.1,1.0,0.85,0.01)
fracs=np.interp(temps,[25,200],[f25,f200])
ratios=(na*wp*fracs)/(nd*wn)
fig2=go.Figure(go.Scatter(x=temps,y=ratios,mode="lines+markers"))
fig2.add_hline(y=1.0,line_dash="dash")
fig2.update_layout(xaxis_title="Temperature (°C)",yaxis_title="QP / QN",title="What-if: ionization-driven charge-balance shift")
st.plotly_chart(fig2,use_container_width=True)
st.warning("This is a what-if visualization, NOT a validated dynamic incomplete-ionization model. 🟣 Exact kinetics require primary-source verification.")

st.subheader("5 · Conference notes awaiting verification")
for item in kb.get("pending_verification",[]):
    st.checkbox(item,value=False)

st.subheader("6 · Questions worth asking")
st.markdown("""
- Does room-temperature optimum charge balance remain optimum at 175–200°C?
- What sets the practical crossover between channeling implantation and trench filling?
- How does SJ field redistribution move SC / avalanche hot spots?
- Which trench-MOS process modules can be reused for SJ?
- How wide is the manufacturable charge-balance window across an 8-inch wafer?
""")
