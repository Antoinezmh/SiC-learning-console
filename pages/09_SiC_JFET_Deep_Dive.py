import streamlit as st
st.title("⚡ SiC JFET Deep Dive")
st.write("Bulk-channel device controlled by PN-junction depletion; no SiC/SiO₂ inversion channel is required in the main current path.")
st.markdown("**More reverse-biased VGS → wider depletion → narrower channel → pinch-off → lower ID.** Conventional power JFET is normally-on at VGS=0.")
st.latex(r"R_{on,JFET}\approx R_{channel,bulk}+R_{drift}+R_{sub}+R_{contact}")
st.markdown("### System approaches
1. Normally-on JFET
2. Dual-drive/system-assisted JFET
3. Cascode: SiC JFET + low-voltage Si MOSFET

Protection/SSCB applications make conduction loss, fault behavior and fail-safe architecture especially important.")