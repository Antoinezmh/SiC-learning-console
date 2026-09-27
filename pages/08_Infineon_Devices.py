import streamlit as st
st.title("🏭 Infineon SiC Technology Map")
st.info("Architecture learning map, not a live product catalog; verify current specs against official datasheets.")
for f in ["SiC SBD","CoolSiC MOSFET generations","CoolSiC JFET","Cascode concepts","Hybrid Si/SiC concepts","SiC modules"]:
 with st.expander(f):
  st.write("Ask: which physical bottleneck is removed? What changes in RON, switching, oxide/body-diode stress, ruggedness and manufacturability?")