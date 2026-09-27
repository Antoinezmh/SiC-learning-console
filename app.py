import streamlit as st
st.set_page_config(page_title="SiC Learning Console",page_icon="⚡",layout="wide")
st.title("⚡ SiC Learning & R&D Console")
st.caption("Material → Epitaxy → Defect → Process → MOS → Device → Reliability → Module → System")
st.markdown("""### Evidence discipline
🟢 **Tutorial direct** · 🔵 **Tutorial-derived** · 🟠 **Engineering model** · 🟣 **Frontier / verify**
""")
a,b,c,d=st.columns(4);a.metric("Core layers","9");b.metric("Deep dives","7+");c.metric("Source pack","ICSCRM 2026");d.metric("Mode","Learn → Model → Design")
st.info("Knowledge node: Physics → Evidence → Device impact → Engineering action.")