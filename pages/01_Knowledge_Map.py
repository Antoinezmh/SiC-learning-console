import streamlit as st
st.title("🗺️ SiC Knowledge Map")
layers=[
("1. Material","4H-SiC bandgap, critical field, anisotropic transport"),
("2. Crystal & Epitaxy","PVT bulk growth, step-flow epitaxy, doping and macrodefects"),
("3. Defects","VC / Z1/2, BPD, TED/TSD, stacking faults"),
("4. Process","implantation, oxidation, anneal, trench/SJ process routes"),
("5. MOS Interface","free vs trapped charge, mobility, oxide/interface physics"),
("6. Device","SBD, MOSFET, trench, JFET, SJ, IGBT"),
("7. Reliability","BTI, GSI, bipolar degradation, avalanche/SC"),
("8. Module","bonding, thermal path, parasitic inductance, gate drive"),
("9. System","converter, protection, efficiency, power density")
]
for name,desc in layers:
    with st.expander(name): st.write(desc)
st.subheader("Cross-layer reasoning")
st.write("Example: BPD → carrier recombination → stacking-fault expansion → lifetime/on-state degradation → body-diode design and qualification strategy. 🔵 Tutorial-derived")
