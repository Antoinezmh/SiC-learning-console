import streamlit as st
st.title("🔬 MOS / Trench / FinFET")
st.latex(r"\mu_{ch}\approx\mu_{free}\frac{n_{free}}{n_{free}+n_{trap}}")
st.caption("🟠 Teaching model; tutorial uses Split C–V + MOS-Hall to separate free/trapped charge.")
st.latex(r"R_{on}=R_{ch}+R_{acc}+R_{JFET}+R_{drift}+R_{sub}+R_{contact}")
st.markdown("""### Design questions
- Sidewall plane and channel transport?
- Rch improvement vs total RON?
- Trench-corner oxide field?
- Shielding vs RON tradeoff?
- Dominant term at 175–200°C?
### Fin structures
Useful research lens for electrostatics, trapping and mobility. Exact performance claims require primary-paper verification. 🟣""")