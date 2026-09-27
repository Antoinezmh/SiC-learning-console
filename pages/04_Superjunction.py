import streamlit as st
st.title("🏗️ SiC Superjunction")
st.write("SiC SJ uses alternating p/n charge regions to reshape the electric field and relax the conventional unipolar drift-region tradeoff. 🔵 Tutorial-derived")
st.subheader("Charge-balance teaching model")
st.latex(r"Q_N=qN_DW_N")
st.latex(r"Q_P=qN_A^-W_P")
st.latex(r"\Delta Q=\frac{Q_N-Q_P}{Q_N}")
st.caption("🟠 Engineering model; N_A⁻ highlights that incomplete ionization can matter.")
route=st.radio("Process route",["High-energy channeling implantation","Trench filling"])
if route.startswith("High"):
    st.write("Tutorial: advantageous in process cycle time. 🟢 Tutorial direct")
else:
    st.write("Tutorial: becomes more attractive as columns become deeper. 🟢 Tutorial direct")
st.markdown("""
### Engineering checklist
**Static:** BV, RON, charge imbalance tolerance, temperature dependence  
**Dynamic:** Qrr, capacitance, transient field redistribution  
**Ruggedness:** short circuit, avalanche, forward-current tolerance  
**Manufacturing:** alignment, activation, column depth/uniformity, epi/process cycle time
""")
