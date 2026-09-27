import streamlit as st
st.title("🏗️ SiC Superjunction — Deep Dive")
st.success("Core idea: P/N charge compensation reshapes the drift-region electric field, enabling higher N-column doping and lower specific on-resistance.")
st.subheader("1 · Charge balance")
c1,c2=st.columns(2)
with c1:
 st.latex(r"Q_N=qN_DW_N");st.latex(r"Q_P=qN_A^-W_P")
with c2:
 st.latex(r"\Delta Q=\frac{Q_N-Q_P}{Q_N}");st.write("Ideal design targets QN ≈ QP. Effective ionized acceptor density matters, not only nominal Al dose. 🟠")
st.subheader("2 · Why SiC SJ is difficult")
st.markdown("""**Physics → Process → Product**
- Deep, narrow and uniform P/N columns
- Charge-balance sensitivity to dose, geometry and activation
- P-type incomplete ionization and temperature dependence
- Edge termination must coexist with SJ field shaping
- Wafer/lot uniformity and process window matter as much as best-die RON
""")
st.subheader("3 · Two process routes from the tutorial")
route=st.radio("Compare route",["High-energy channeling implantation","Trench filling / epitaxial fill"])
if route.startswith("High"):
 st.write("Tutorial conclusion: attractive from process-cycle-time perspective. Watch implant depth, damage, activation and lateral/vertical dose control. 🟢/🔵")
else:
 st.write("Tutorial conclusion: becomes more attractive as columns get deeper. Watch deep-trench profile, fill defects, interface quality and uniformity. 🟢/🔵")
st.subheader("4 · Device evaluation matrix")
st.dataframe({"Layer":["Static","Dynamic","Ruggedness","Manufacturing"],"Key metrics":["BV, Ron,sp, charge-balance window, Ron(T)","Qrr, Coss/Crss, switching field redistribution","SC, avalanche, forward-current tolerance","column depth, activation, uniformity, yield, cycle time"]},hide_index=True)
st.subheader("5 · Temperature question")
temp=st.slider("Junction temperature (°C)",25,200,175,25)
imb=st.slider("Illustrative charge imbalance ΔQ (%)",-20,20,0)
st.metric("Illustrative |ΔQ|",f"{abs(imb)} %")
st.caption(f"At {temp}°C ask whether acceptor ionization shifts effective P-column charge. This widget is conceptual, not a calibrated device model. 🟠")
st.subheader("6 · Roadmap questions")
st.markdown("""- Where is the practical crossover: channeling implant → trench fill?
- Does optimum room-temperature charge balance remain optimum at 175–200°C?
- How does SJ move the short-circuit/avalanche hot spot?
- What process modules can be reused from trench MOSFET manufacturing?
- At what voltage/column depth does SiC IGBT become more attractive? Tutorial explicitly flags IGBT potential for ~10 kV class and above. 🟢
""")