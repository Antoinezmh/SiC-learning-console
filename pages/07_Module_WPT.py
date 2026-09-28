import streamlit as st
from sic_ui import inject_styles
inject_styles()
st.title("📦 Module / Low-L / Gate Drive")
st.caption("Takahashi 周日教程：模块的热、键合和回路。不排进体单晶到栅氧的制作顺序。")
st.write("Tutorial priorities: reliable bonding, thermal conductivity, low inductance and advanced gate drive. 🟢")
st.latex(r"I_{CM}=C_{par}\frac{dV}{dt}");st.caption("🟠 Engineering model")
st.markdown("**Design loop:** commutation L → gate/Kelvin L → thermal spreading → dv/dt EMI/common-mode → package/driver/protection co-design.")