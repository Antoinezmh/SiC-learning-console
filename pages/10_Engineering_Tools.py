import streamlit as st
from sic_ui import inject_styles
inject_styles()
import numpy as np
import plotly.graph_objects as go
st.title("🧮 Engineering Tools")
t1,t2,t3=st.tabs(["Unipolar limit","RON budget","Common-mode current"])
with t1:
 bv=st.slider("VB (V)",600,10000,1200,100);ron=2.8e-11*bv**2.28;st.metric("Ron,sp",f"{ron*1e3:.2f} mΩ·cm²")
 vs=np.linspace(600,10000,150);st.plotly_chart(go.Figure(go.Scatter(x=vs,y=2.8e-11*vs**2.28*1e3)),use_container_width=True)
with t2:
 vals={k:st.number_input(k+" (mΩ)",0.,100.,1.) for k in ["Rch","Racc","RJFET","Rdrift","Rsub","Rcontact"]};st.metric("Total",f"{sum(vals.values()):.2f} mΩ")
with t3:
 c=st.number_input("Cpar (pF)",1.,5000.,100.);dv=st.number_input("dv/dt (V/ns)",1.,500.,50.);st.metric("Icm",f"{c*1e-12*dv*1e9:.3f} A")
st.caption("🟠 Teaching models; validate before design sign-off.")