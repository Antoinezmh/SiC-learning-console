import streamlit as st
import numpy as np
import plotly.graph_objects as go
from calculators.sj_route_comparator import ANCHORS,interpolate_cycle_time,crossover
from utils.content_loader import load_yaml

st.title("🏭 SJ Process Route Comparator")
st.caption("🟢 Harada measured anchors · 🔷 literature constraints · 🟠 extrapolation / fab interpretation")

cfg=load_yaml("content/process/sj_route_comparator.yaml")
depth=st.slider("P/N column depth (µm)",3.,25.,5.,.5)
voltage=st.radio("Reference voltage class",["1.2 kV","3.3 kV","6.5 kV / exploratory"],horizontal=True)
st.info("Cycle-time values are normalized process time from wafer loading to unloading — NOT manufacturing cost; equipment depreciation is excluded.")

routes=list(ANCHORS)
vals={r:interpolate_cycle_time(r,depth) for r in routes}
cols=st.columns(4)
for c,r in zip(cols,routes):
    c.metric(r,f"{vals[r]:.2f}",help="5/10 µm are tutorial anchors; other depths are linear engineering extrapolation.")

xs=np.linspace(3,25,150)
fig=go.Figure()
for r in routes:
    fig.add_trace(go.Scatter(x=xs,y=[interpolate_cycle_time(r,x) for x in xs],name=r))
    fig.add_trace(go.Scatter(x=[5,10],y=[ANCHORS[r][5],ANCHORS[r][10]],mode="markers",showlegend=False))
fig.add_vline(x=5,line_dash="dot");fig.add_vline(x=10,line_dash="dot")
fig.update_layout(xaxis_title="Column depth (µm)",yaxis_title="Normalized cycle time",title="Measured anchors + linear extrapolation")
st.plotly_chart(fig,use_container_width=True)
st.warning("🟠 Only 5 and 10 µm points are Tutorial-direct. The connecting/extrapolated lines are intentionally simple trend models, not fab forecasts.")

ct=crossover("TFE","Channeling")
if ct: st.write(f"**Linear-anchor model crossover (TFE vs Channeling): ~{ct:.1f} µm.** 🟠 Do not treat as a measured technology boundary.")

st.subheader("Fab-readiness view")
rows=[]
for r in routes:
    d=cfg["routes"][r]
    f=d["fab_interpretation"]
    rows.append({"Route":r,"Tool family":f["tool_family"],"Integration burden":f["capex_level"],"Key risks":" / ".join(f["risks"])})
st.dataframe(rows,hide_index=True,use_container_width=True)

st.subheader("Performance evidence is architecture-dependent")
st.markdown("""
The following Harada SJ results are useful **benefit anchors**, but should not be assigned as intrinsic scores to every fabrication route:
- 🟢 DI-SJUMOS: ΔVf **0.48% max** in the cited Al+P double-implant study.
- 🟢 Semi-SJ short-circuit: **15.0 µs vs 13.0 µs** UMOS in the cited comparison.
- 🟢 At the cited RonA comparison point: ESC advantage **+13% RT / +53% @175°C**.
- 🟢 3.3 kV-class SJ + improved JTE: avalanche current density **1000 A/cm²**, EAS about **13.4 J/cm²**.

These are not apples-to-apples route-level ratings. Device structure, termination, lifetime control and process details differ.
""")

st.subheader("Decision lens")
st.dataframe({
 "Question":["Fastest measured process time?","Deep-column scalability?","Existing-line reuse?","Most sensitive hidden variable?"],
 "Look at":["5/10 µm tutorial anchors","TFE depth trend + trench fill quality","actual fab toolset, not generic CapEx score","alignment / void / damage / repeated-module variation"]
},hide_index=True,use_container_width=True)
