import streamlit as st
from sic_ui import inject_styles
inject_styles()
st.title("🛡️ Reliability / BTI / GSI / REDR")
st.caption("Grossner 周日教程：退化机理。这里的陷阱分类不充当晶圆工艺看板上的 Dit 合格线。")
st.markdown("**Stress → Material change → Location → Electrical signature → Physical model → Independent verification**")
st.write("Tutorial covers interface/border/bulk/near-interface defects, SRH kinetics, BTI, GSI and tunneling-assisted oxide-trap interactions. 🟢")
st.warning("One electrical symptom can have several physical origins; do not assign mechanism from ΔVth alone.")
st.write("Extended non-radiative multiphonon modeling is discussed in connection with dynamic recombination-enhanced defect reactions. 🟢")