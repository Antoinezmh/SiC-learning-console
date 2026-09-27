import streamlit as st
import numpy as np
import plotly.graph_objects as go
from calculators.sj_monte_carlo import simulate

st.title("🎲 SJ Monte Carlo Process Window")
st.caption("🟠 Statistical sensitivity explorer — not a fab-qualified yield predictor.")
n=st.select_slider("Samples",options=[5000,10000,25000,50000,100000],value=50000)
c1,c2,c3=st.columns(3)
with c1:
 nd=st.number_input("ND nominal",1e15,1e18,5e16,format="%.2e");snd=st.slider("σ ND (%)",0.,15.,5.,0.5)
 na=st.number_input("NA nominal",1e15,1e19,5e16,format="%.2e");sna=st.slider("σ NA (%)",0.,15.,5.,0.5)
with c2:
 wn=st.number_input("WN nominal (µm)",0.1,20.,2.);wp=st.number_input("WP nominal (µm)",0.1,20.,2.)
 scd=st.number_input("CD σ (µm)",0.,1.,0.05,0.01)
with c3:
 ion=st.slider("Effective P ionization",0.1,1.,1.,0.01)
 sang=st.number_input("Implant-angle σ (deg)",0.,5.,0.1,0.05)
 sens=st.number_input("Angle sensitivity / deg",0.,0.2,0.0,0.005)
 lim=st.slider("Charge-balance acceptance ± (%)",1,20,10)
ratio,ok,angle=simulate(n,nd,na,wn,wp,snd,sna,scd,ion,sang,sens,lim)
st.metric("Estimated in-window fraction",f"{ok.mean()*100:.2f}%")
fig=go.Figure(go.Histogram(x=ratio,nbinsx=100))
fig.add_vline(x=1-lim/100,line_dash="dash");fig.add_vline(x=1+lim/100,line_dash="dash")
fig.update_layout(xaxis_title="QP/QN",yaxis_title="Count")
st.plotly_chart(fig,use_container_width=True)
st.warning("Angle sensitivity is user-defined because the tutorial establishes alignment criticality but does not provide a universal angle→dose-transfer law.")
