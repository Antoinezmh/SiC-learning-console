import streamlit as st
st.title("⚡ SiC JFET Deep Dive")
st.markdown("""
### Core physics
A SiC JFET is a **bulk-channel device** controlled by PN-junction depletion. It does not require a SiC/SiO₂ inversion channel in the main current path.

**VGS becomes more reverse-biased → depletion width expands → channel narrows → pinch-off → ID falls.**

A conventional power JFET is **normally on** at VGS = 0.
""")
st.subheader("Conduction path comparison")
c1,c2=st.columns(2)
with c1:
    st.markdown("**MOSFET**")
    st.write("Source → inversion channel → accumulation/JFET region → drift → drain")
    st.write("Interface traps and channel mobility directly affect RON.")
with c2:
    st.markdown("**JFET**")
    st.write("Source → bulk SiC channel → drift → drain")
    st.write("Avoids the inversion-channel interface penalty.")
st.latex(r"R_{on,JFET}\approx R_{channel,bulk}+R_{drift}+R_{sub}+R_{contact}")
st.caption("🟠 Engineering model")
st.subheader("Three system approaches")
st.markdown("""
1. **Normally-on JFET** — simplest current path and low conduction resistance; requires fail-safe architecture.
2. **Dual-drive/system-assisted JFET** — separates normal operation and fault-management requirements.
3. **Cascode** — pairs a SiC JFET with a low-voltage Si MOSFET to expose a normally-off, familiar gate interface.

### Why protection is interesting
In solid-state circuit breakers and battery protection, the device may spend most of its life conducting and switch off mainly during faults. This shifts optimization toward ultra-low conduction loss, linear/fault behavior and fail-safe system design.
""")
