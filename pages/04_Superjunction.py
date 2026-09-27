import streamlit as st
import numpy as np
import plotly.graph_objects as go
from utils.content_loader import load_yaml
from calculators.sj_charge_balance import charge_balance, illustrative_ionization_sweep

st.title("🏗️ SiC Superjunction — Design Workbench")
kb=load_yaml("content/tutorials/icscrm2026_superjunction.yaml")
st.caption("Structure → Process → Charge Balance → Temperature → Dynamic Ionization → Ruggedness → Process Window")

st.subheader("1 · Charge-balance workbench")
c1,c2=st.columns(2)
with c1:
    nd=st.number_input("N-column ND (cm⁻³)",1e15,1e18,5e16,format="%.2e")
    wn=st.number_input("N-column width WN (μm)",0.1,20.0,2.0)
with c2:
    na=st.number_input("P-column nominal NA (cm⁻³)",1e15,1e19,5e16,format="%.2e")
    wp=st.number_input("P-column width WP (μm)",0.1,20.0,2.0)
    ion=st.slider("Effective acceptor ionization fraction — what-if",0.10,1.00,0.70,0.01)
res=charge_balance(nd,wn,na,wp,ion)
a,b=st.columns(2);a.metric("QP / QN",f"{res['qp_over_qn']:.3f}");b.metric("ΔQ / QN",f"{res['imbalance']*100:.2f} %")
st.caption("🟠 Engineering model. The ionization fraction is user-specified rather than fitted to a calibrated Al model.")

st.subheader("2 · Dynamic incomplete ionization — 🟢 Tutorial direct")
st.markdown("""Harada's tutorial explicitly states that **delayed ionization causes temporary p-column charge imbalance during turn-off transients**. It also connects delayed ionization with **soft reverse recovery of the body diode**.

Primary references listed by the tutorial:
- D. Nazareno et al., IEEE TED 65, 4469 (2018)
- D. Iizasa et al., SST 40, 125010 (2025)
- T. Tawara et al., MSSP 176, 108324 (2024)
""")
temps=np.array([25,75,125,175,200])
f25=st.slider("Illustrative ionization fraction @25°C",0.1,1.0,0.55,0.01)
f200=st.slider("Illustrative ionization fraction @200°C",0.1,1.0,0.85,0.01)
fracs,ratios=illustrative_ionization_sweep(nd,wn,na,wp,temps,f25,f200)
fig=go.Figure(go.Scatter(x=temps,y=ratios,mode="lines+markers"))
fig.add_hline(y=1.0,line_dash="dash");fig.update_layout(xaxis_title="Temperature (°C)",yaxis_title="QP / QN",title="What-if visualization: ionization-driven charge-balance shift")
st.plotly_chart(fig,use_container_width=True)
st.warning("🟠 The plotted temperature interpolation is a teaching what-if model. The existence of dynamic incomplete ionization is tutorial-direct; this numerical curve is NOT the Nazareno model.")

st.subheader("3 · Bipolar degradation suppression — 🟢 Tutorial direct")
st.dataframe({
 "Structure":["Conventional UMOS","SI-SJUMOS","DI-SJUMOS (Al + P)"],
 "ΔVf":["21.2%","5.9%","0.48% max."],
 "Tutorial interpretation":["baseline","SJ-UMOS degrades less, but remains insufficient at high current","Al + P double implantation introduces many point defects"]
},hide_index=True,use_container_width=True)
st.caption("Harada tutorial slide 30 / PDF p.137; K. Takenaka et al., JJAP 64, 02SP43 (2025).")

st.subheader("4 · Process-route radar")
st.dataframe({
 "Route":["Multi-epi","High-energy implantation","Channeling implantation","Trench filling / epi fill"],
 "Engineering focus":["repeat epi / dose control","depth / damage / activation","deep implant via crystal channeling","deep trench / fill / defects"],
 "Evidence":["🟣 exact cycle-time values pending","🟣 details pending","🟢 cycle-time advantage stated","🟢 increasingly attractive for deeper columns"]
},hide_index=True,use_container_width=True)

st.subheader("5 · Productization matrix")
st.dataframe({
 "Layer":["Structure","Process","Static","Dynamic","Ruggedness","Manufacturing"],
 "Key questions":["column width/depth, asymmetry","implant/fill, activation, damage","BV, Ron,sp, Ron(T)","Qrr, transient charge balance, Coss/Crss","SC, avalanche, body diode","uniformity, process window, yield, cycle time"]
},hide_index=True,use_container_width=True)

st.subheader("6 · 8-inch / product questions")
st.markdown("""- How wide is the allowable **QP/QN process window** across wafer and lot?
- Does the optimum static charge balance also optimize **turn-off transient** behavior?
- How should p-column ionization kinetics enter TCAD?
- Can implant-induced point defects suppress bipolar degradation without unacceptable mobility/lifetime penalties?
- Where is the practical crossover between channeling implantation and trench filling?
- Which trench-MOS process modules can be inherited by an SJ platform?
""")
