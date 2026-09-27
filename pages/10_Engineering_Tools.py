import streamlit as st
import numpy as np
import plotly.graph_objects as go
st.title("🧮 Engineering Tools")
tab1,tab2,tab3=st.tabs(["Unipolar limit","RON budget","Common-mode current"])
with tab1:
    bv=st.slider("Breakdown voltage VB (V)",600,10000,1200,100)
    ron=2.8e-11*bv**2.28
    st.metric("Tutorial empirical Ron,sp",f"{ron*1e3:.2f} mΩ·cm²")
    vs=np.linspace(600,10000,150); rs=2.8e-11*vs**2.28
    fig=go.Figure(go.Scatter(x=vs,y=rs*1e3)); fig.update_layout(xaxis_title="VB (V)",yaxis_title="Ron,sp (mΩ·cm²)")
    st.plotly_chart(fig,use_container_width=True)
with tab2:
    vals={}
    for k in ["Rch","Racc","RJFET","Rdrift","Rsub","Rcontact"]:
        vals[k]=st.number_input(k+" (mΩ)",0.0,100.0,1.0)
    total=sum(vals.values()); st.metric("Total RON",f"{total:.2f} mΩ")
    fig=go.Figure(go.Bar(x=list(vals.keys()),y=list(vals.values()))); st.plotly_chart(fig,use_container_width=True)
with tab3:
    c=st.number_input("Parasitic capacitance (pF)",1.0,5000.0,100.0)
    dv=st.number_input("dv/dt (V/ns)",1.0,500.0,50.0)
    icm=c*1e-12*dv*1e9
    st.metric("Peak displacement current",f"{icm:.3f} A")
st.caption("🟠 These calculators are engineering teaching models; validate assumptions before design sign-off.")
