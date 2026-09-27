import streamlit as st
st.title("🧬 Defects & Bipolar Degradation")
st.markdown("""
### Defect chain
**BPD + carrier recombination → stacking-fault expansion → lifetime / on-state degradation**

The tutorial emphasizes BPD as the critical extended defect for bipolar degradation, while TED/TSD impact is comparatively small. 🟢 Tutorial direct

### Carbon vacancy / lifetime
Z1/2 is associated with the carbon vacancy **V_C**. Carbon-vacancy elimination by oxidation/annealing or carbon-related treatment can strongly enhance minority-carrier lifetime. 🟢 Tutorial direct

Tutorial example: lifetime evolves from roughly **1.8 μs → 28.1 μs → 34.2 μs** after vacancy elimination and surface passivation. 🟢 Tutorial direct

### Engineering lever
A heavily doped n+ epitaxial recombination-enhancing layer can prevent holes from reaching the substrate and suppress stacking-fault expansion. 🟢 Tutorial direct
""")
st.subheader("R&D question generator")
for q in ["What BPD density is tolerable for the target chip area?","Where should minority-carrier lifetime be high vs deliberately short?","How does body-diode mission profile change degradation risk?"]:
    st.checkbox(q)
