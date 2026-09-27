import streamlit as st
st.title("📚 ICSCRM 2026 Tutorial Pack")
talks={
"Kimoto — Fundamentals of SiC Power Semiconductors":"Material/device physics; bulk & epitaxy; carrier lifetime; extended defects; MOS carrier transport; remaining issues.",
"Friedrichs — SiC in Modern Power Electronics":"How SiC changes converter efficiency, power density and system architecture.",
"Harada — Next Generation SiC Power Devices":"Superjunction process routes, high-voltage devices and emerging architectures.",
"Grossner — Material Perturbation to Device Degradation":"Defect kinetics, oxide traps, BTI/GSI and degradation modeling.",
"Takahashi — SiC Power Modules":"Thermal, bonding, low-inductance integration, gate drive and advanced module concepts."
}
for k,v in talks.items():
    with st.expander(k): st.write(v); st.caption("🟢 Tutorial direct")
st.subheader("Key numerical anchors")
st.code("Ron,sp = 2.8×10⁻¹¹ × VB^2.28  [Ω·cm²], VB in V")
st.write("PVT growth: source ~2300–2500 °C; seed ~2200–2400 °C; pressure ~0.5–2 kPa; growth ~0.3–1 mm/h. 🟢 Tutorial direct")
st.write("Typical SiC epitaxy: ~1600–1750 °C, 3–20 kPa, growth ~10–30 μm/h. 🟢 Tutorial direct")
st.warning("This repository intentionally separates tutorial statements from later engineering interpretation. Exact frontier claims should be verified against primary papers before being promoted to 'Tutorial direct'.")
