import streamlit as st
st.title("🗺️ SiC Knowledge Map")
layers=[("Material","4H-SiC, critical field, anisotropy"),("Crystal & Epitaxy","PVT, step-flow, doping, macrodefects"),("Defects","VC/Z1/2, BPD, TED/TSD, stacking faults"),("Process","implant, oxidation, anneal, trench/SJ"),("MOS Interface","free/trapped charge, mobility"),("Device","SBD, MOSFET, trench, JFET, SJ, IGBT"),("Reliability","BTI, GSI, bipolar degradation, SC/avalanche"),("Module","thermal, bonding, parasitics, gate drive"),("System","converter, protection, efficiency, density")]
for n,d in layers:
    with st.expander(n):st.write(d)
st.info("Cross-layer example: BPD → recombination → stacking-fault expansion → lifetime/on-state degradation → body-diode strategy. 🔵")