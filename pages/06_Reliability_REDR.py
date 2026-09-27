import streamlit as st
st.title("🛡️ Reliability / BTI / GSI / REDR")
st.markdown("""
A useful reliability workflow is:

**Stress → Material change → Location → Electrical signature → Physical model → Independent verification**

The tutorial covers interface/border/bulk/near-interface defects, SRH capture/emission, BTI, GSI and tunneling-assisted oxide-trap interactions. 🟢 Tutorial direct
""")
st.subheader("Mechanism discipline")
st.warning("One electrical symptom can have several physical origins. Do not assign a mechanism from ΔVth alone.")
st.write("The tutorial discusses an extended non-radiative multiphonon (eNMP) framework in connection with dynamic recombination-enhanced defect reactions. 🟢 Tutorial direct")
st.markdown("""
### Characterization matrix
- DC/AC bias-temperature stress
- recovery kinetics
- temperature activation
- charge pumping / C–V where applicable
- gate leakage
- switching-history dependence
- independent structural/material evidence

The goal is **converging evidence**, not a single fitted curve. 🔵 Tutorial-derived
""")
