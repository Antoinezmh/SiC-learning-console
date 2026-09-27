import streamlit as st
st.title("📦 Module / Low-L / Gate Drive")
st.write("Tutorial priorities: high-reliability bonding, high thermal conductivity, low inductance and advanced gate drive. 🟢 Tutorial direct")
st.subheader("Common-mode displacement-current model")
st.latex(r"I_{CM}=C_{par}\frac{dV}{dt}")
st.caption("🟠 Engineering model")
st.markdown("""
### Module design loop
1. Minimize commutation-loop inductance
2. Control gate-loop inductance and Kelvin-source path
3. Engineer thermal spreading for smaller SiC dies
4. Manage high dv/dt EMI and common-mode paths
5. Co-design package + driver + protection

Tutorial examples include double-sided and 3D integration concepts, Ag-sinter-related packaging, embedded power modules and high-temperature operation. 🟢 Tutorial direct
""")
