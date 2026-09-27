import streamlit as st
import numpy as np
import plotly.graph_objects as go
from calculators.sj_process_window import charge_ratio_grid,within_window

st.title("🎯 SJ Process Window")
st.caption("First-order manufacturing sensitivity tool — not calibrated BV/yield prediction. 🟠")
c1,c2=st.columns(2)
with c1:
 nd=st.number_input("ND",1e15,1e18,5e16,format="%.2e")
 wn=st.number_input("WN nominal (μm)",0.1,20.,2.)
 wt=st.slider("Width variation ± (%)",1,20,5)
with c2:
 na=st.number_input("NA",1e15,1e19,5e16,format="%.2e")
 wp=st.number_input("WP nominal (μm)",0.1,20.,2.)
 dt=st.slider("Dose variation ± (%)",1,20,5)
ion=st.slider("Effective P ionization fraction",0.1,1.,1.,0.01)
allow=st.slider("Allowed |QP/QN − 1| (%)",1,20,5)
x,y,z=charge_ratio_grid(nd,na,wn,wp,wt,dt,ion)
mask=within_window(z,allow)
st.metric("Grid fraction inside selected balance window",f"{mask.mean()*100:.1f}%")
fig=go.Figure(go.Heatmap(x=x,y=y,z=z,colorbar_title="QP/QN"))
fig.update_layout(xaxis_title="Width perturbation (%)",yaxis_title="Dose perturbation (%)",title="Charge-balance process-window map")
st.plotly_chart(fig,use_container_width=True)
st.warning("The opposing P/N perturbation is deliberately conservative for sensitivity exploration. Replace with fab-specific statistical distributions for yield prediction.")
