import streamlit as st
import numpy as np
import plotly.graph_objects as go
from calculators.unipolar_limit import tutorial_ron_sp
from calculators.sj_charge_balance import charge_balance

st.title("🧮 Engineering Tools")
t1,t2,t3,t4=st.tabs(["Unipolar limit","RON budget","SJ charge balance","Common-mode current"])
with t1:
    bv=st.slider("VB (V)",600,10000,1200,100)
    ron=tutorial_ron_sp(bv)
    st.metric("Tutorial empirical Ron,sp",f"{ron*1e3:.2f} mΩ·cm²")
    vs=np.linspace(600,10000,150)
    st.plotly_chart(go.Figure(go.Scatter(x=vs,y=[tutorial_ron_sp(v)*1e3 for v in vs])),use_container_width=True)
with t2:
    vals={k:st.number_input(k+" (mΩ)",0.,100.,1.) for k in ["Rch","Racc","RJFET","Rdrift","Rsub","Rcontact"]}
    st.metric("Total RON",f"{sum(vals.values()):.2f} mΩ")
with t3:
    nd=st.number_input("ND (cm⁻³)",1e15,1e18,5e16,format="%.2e",key="sjnd")
    wn=st.number_input("WN (μm)",0.1,20.,2.,key="sjwn")
    na=st.number_input("NA (cm⁻³)",1e15,1e19,5e16,format="%.2e",key="sjna")
    wp=st.number_input("WP (μm)",0.1,20.,2.,key="sjwp")
    fi=st.slider("Effective acceptor ionization",0.1,1.,0.7,0.01,key="sjfi")
    r=charge_balance(nd,wn,na,wp,fi)
    st.metric("QP/QN",f"{r['qp_over_qn']:.3f}");st.metric("ΔQ/QN",f"{r['imbalance']*100:.2f}%")
    st.caption("🟠 First-order charge-balance calculator; not a BV/process calibration.")
with t4:
    c=st.number_input("Cpar (pF)",1.,5000.,100.);dv=st.number_input("dv/dt (V/ns)",1.,500.,50.)
    st.metric("Icm",f"{c*1e-12*dv*1e9:.3f} A")
