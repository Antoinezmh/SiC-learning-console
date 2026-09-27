import streamlit as st
st.title("📚 ICSCRM 2026 Tutorial Pack")
talks={"Kimoto — Fundamentals":"Material/device physics; bulk/epi; lifetime; extended defects; MOS transport.","Friedrichs — Power Electronics":"Efficiency, density and system architecture.","Harada — Next Generation Devices":"Superjunction routes, high-voltage devices, emerging architectures.","Grossner — Degradation":"Defect kinetics, oxide traps, BTI/GSI.","Takahashi — Modules":"Thermal, bonding, low-L integration, gate drive."}
for k,v in talks.items():
    with st.expander(k):st.write(v);st.caption("🟢 Tutorial direct")
st.code("Ron,sp = 2.8×10⁻¹¹ × VB^2.28  [Ω·cm²], VB in V")
st.write("PVT: source ~2300–2500°C; seed ~2200–2400°C; ~0.5–2 kPa; ~0.3–1 mm/h. 🟢")
st.write("Epitaxy: ~1600–1750°C; 3–20 kPa; ~10–30 μm/h. 🟢")