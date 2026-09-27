import streamlit as st
st.title("🔬 MOS / Trench / FinFET")
st.subheader("MOS transport decomposition")
st.latex(r"\mu_{ch}\approx \mu_{free}\frac{n_{free}}{n_{free}+n_{trap}}")
st.caption("🟠 Engineering teaching model. Tutorial discusses Split C–V and MOS-Hall separation of free/trapped charge.")
st.write("Split C–V provides total mobile + trapped charge information; MOS-Hall provides Hall mobility and free-carrier density. 🟢 Tutorial direct")
st.subheader("Trench MOSFET RON budget")
st.latex(r"R_{on}=R_{ch}+R_{acc}+R_{JFET}+R_{drift}+R_{sub}+R_{contact}")
st.caption("🟠 Engineering model")
st.markdown("""
### Design questions
- Which trench sidewall crystal plane carries the channel?
- How much of RON improvement is truly channel-related?
- What is the oxide electric-field penalty at trench corners?
- Can shielding geometry decouple low RON from oxide reliability?
- Which parameters remain temperature-sensitive at 175–200 °C?

### Fin structures
Fin-based channels are useful as a research lens for separating electrostatic confinement, interface trapping and effective mobility. Exact geometry/performance numbers should be attached to primary papers before use. 🟣 Frontier
""")
