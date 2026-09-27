import streamlit as st
import numpy as np
import plotly.graph_objects as go
from calculators.sj_physics import ideal_1d_unipolar,idealized_sj,heuristic_imbalance_bv

st.title("📐 SJ Physics & Voltage Roadmap")
st.caption("🔷 literature theory · 🟠 idealized model · 🟢 tutorial evidence")

tab1,tab2,tab3=st.tabs(["Ideal scaling","Imbalance sensitivity","Voltage roadmap"])
with tab1:
    vb=st.slider("Breakdown-voltage target (V)",600,10000,3300,100)
    wn=st.slider("Half-pillar width Wn (µm)",0.2,10.,2.,0.1)
    a=ideal_1d_unipolar(vb);b=idealized_sj(vb,wn)
    c1,c2=st.columns(2)
    c1.metric("1-D ideal Ron,sp",f"{a['ron_ohm_cm2']*1e3:.2f} mΩ·cm²")
    c2.metric("Idealized SJ Ron,sp",f"{b['ron_ohm_cm2']*1e3:.2f} mΩ·cm²")
    st.write(f"Idealized column length: {b['column_um']:.1f} µm; lateral-depletion ND ceiling: {b['nd_max_cm3']:.2e} cm⁻³")
    st.warning("🟠 Idealized scaling only. SiC anisotropic impact ionization, termination and 2-D field crowding require TCAD/validated analytical models.")
with tab2:
    ar=st.slider("Aspect ratio L/Wn",2.,40.,10.,0.5)
    k=st.slider("Heuristic sensitivity k",0.1,3.,1.,0.1)
    d=np.linspace(-.2,.2,201)
    y=np.array([heuristic_imbalance_bv(1,x,ar,k) for x in d])
    fig=go.Figure(go.Scatter(x=d*100,y=y*100))
    fig.update_layout(xaxis_title="Charge imbalance δ (%)",yaxis_title="Vactual / Videal (%)")
    st.plotly_chart(fig,use_container_width=True)
    st.error("🟠 This curve is a heuristic visualization, not the Wang/Napoli/Udrea exact analytical solution.")
with tab3:
    st.dataframe({
      "Voltage":["~1.2 kV","1.2–3.3 kV","3.3–6.5 kV","~10 kV+"],
      "Architecture":["Trench / Semi-SJ exploration","Short/Semi/Full SJ","Full-SJ / HV MOS research","SiC IGBT candidate"],
      "Process":["Channeling / Multi-epi / TFE","Channeling ↔ TFE study","deeper TFE increasingly attractive","thick epi + p-type collector"],
      "Evidence":["🟢+🟠","🟢+🟠","🟢+🟣","🟢 Tutorial"]
    },hide_index=True,use_container_width=True)
    st.info("Voltage boundaries are a research roadmap, not a recommendation that one architecture universally wins.")
