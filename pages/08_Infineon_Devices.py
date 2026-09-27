import streamlit as st
st.title("🏭 Infineon SiC Device Technology Map")
st.info("This page is an architecture-oriented learning map, not a live product catalog. Current product specifications should be verified against official datasheets.")
families=["SiC Schottky Barrier Diode","CoolSiC MOSFET — generation evolution","CoolSiC JFET — normally-on / system variants","Cascode concepts","Hybrid Si/SiC switch concepts","SiC power modules"]
for f in families:
    with st.expander(f):
        if "JFET" in f: st.write("Bulk-channel conduction removes the inversion-channel mobility penalty; system design must handle normally-on behavior.")
        elif "MOSFET" in f: st.write("Track Rch, drift resistance, Crss/Qgd, oxide field, body-diode behavior and ruggedness—not RDS(on) alone.")
        elif "Schottky" in f: st.write("Major SiC value proposition: unipolar reverse recovery behavior and high-voltage blocking.")
        elif "module" in f.lower(): st.write("Device performance only becomes system performance through low-L, thermal and gate-drive co-design.")
        else: st.write("Study the architecture by asking which physical/system bottleneck it is intended to remove.")
st.subheader("Generation-analysis template")
st.dataframe({"Dimension":["Conduction","Switching","Gate oxide","Body diode","Ruggedness","Manufacturing"],"Question":["Where did RON fall?","What changed in Qgd/Crss?","How is Eox controlled?","What is the bipolar-use strategy?","SC/avalanche tradeoff?","What structural/process complexity was added?"]},hide_index=True)
