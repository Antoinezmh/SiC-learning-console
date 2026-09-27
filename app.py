import streamlit as st
st.set_page_config(page_title="SiC Learning Console", page_icon="⚡", layout="wide")
st.title("⚡ SiC Learning & R&D Console")
st.caption("From material physics to device, reliability, packaging and system engineering")
st.markdown("""
### Knowledge Core
**Material → Crystal/Epitaxy → Defect → Process → MOS Interface → Device → Reliability → Module → System**

This console turns the **ICSCRM 2026 Tutorial** into an expandable engineering knowledge system rather than a static summary.

#### Evidence labels
- 🟢 **Tutorial direct** — explicitly supported by the tutorial source
- 🔵 **Tutorial-derived** — synthesis or connection derived from tutorial material
- 🟠 **Engineering model** — simplified equation/model for design exploration
- 🟣 **Frontier** — research direction requiring paper/public-source verification

Use the pages in the sidebar to move from fundamentals to deep dives and engineering tools.
""")
c1,c2,c3,c4=st.columns(4)
c1.metric("Core layers","9"); c2.metric("Deep dives","7+"); c3.metric("Source pack","ICSCRM 2026"); c4.metric("Mode","Learn → Model → Design")
st.info("Design principle: every knowledge node should answer Physics → Evidence → Device impact → Engineering action.")
