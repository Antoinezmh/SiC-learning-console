import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from calculators.sj_design_flow import initial_structure,ron_budget,mesh_hints
from calculators.tcad_doe import full_factorial_3level,to_csv

st.title("🧠 SJ Design Flow & TCAD Copilot")
st.caption("Requirement → Initial Structure → Ron Budget → Risk → TCAD DOE")

st.subheader("1 · Requirement")
c1,c2,c3=st.columns(3)
with c1: vb=st.number_input("Target BV (V)",600,12000,1200,100)
with c2: route=st.selectbox("Process route",["Channeling","MeV implantation","Multi-epi","TFE"])
with c3: margin=st.slider("BV design margin (%)",0,30,12)/100

s=initial_structure(vb,route,margin)
st.subheader("2 · Initial structure 🟠")
a,b,c,d=st.columns(4)
a.metric("Column depth",f"{s['column_um']:.1f} µm")
b.metric("WN / WP",f"{s['wn_um']:.2f} / {s['wp_um']:.2f} µm")
c.metric("ND seed",f"{s['nd_cm3']:.2e} cm⁻³")
d.metric("Target + margin",f"{s['target_with_margin_v']:.0f} V")
st.warning("These are analytical design seeds, not a fabricated-device recommendation. Route-specific widths are adjustable engineering defaults.")

st.subheader("3 · Ron budget")
c1,c2,c3=st.columns(3)
with c1: rch=st.number_input("Rch (mΩ·cm²)",0.,10.,0.04,.01)
with c2: rj=st.number_input("RJFET (mΩ·cm²)",0.,10.,0.,.01)
with c3: rsub=st.number_input("Rsub (mΩ·cm²)",0.,10.,0.10,.01)
budget=ron_budget(s["rdrift_ohm_cm2"],rch,rj,rsub)
fig=go.Figure(go.Bar(x=list(budget)[:-1],y=list(budget.values())[:-1]))
fig.update_layout(yaxis_title="mΩ·cm²",title=f"Total ≈ {budget['Total']:.3f} mΩ·cm²")
st.plotly_chart(fig,use_container_width=True)
st.caption("🟢 Tutorial anchors: Rch≈0.04 and Rsub≈0.10 mΩ·cm² under Harada slide-7 assumptions. Rdrift here is 🟠 idealized SJ model.")

st.subheader("4 · Mesh starting hints 🟠")
st.json(mesh_hints(s["wn_um"],s["column_um"]))

st.subheader("5 · TCAD DOE — 27 runs 🟠")
overlay=st.number_input("Overlay level ± (µm)",0.,1.,0.10,.01)
rows=full_factorial_3level(s["na_cm3"],s["wp_um"],overlay)
df=pd.DataFrame(rows)
st.dataframe(df,use_container_width=True,hide_index=True)
st.download_button("Download DOE CSV",to_csv(rows),"sj_tcad_doe.csv","text/csv")
st.info("Extract at minimum: BV, Ron, peak E-field/impact-ionization location, and short-circuit hotspot. Add Qrr/dynamic ionization in transient DOE.")
