import streamlit as st
import numpy as np
import plotly.graph_objects as go
from utils.principle_ui import evidence_badge,causal_chain,takeaway,why_it_matters

st.title("🔍 SJ Principle Explorer")
st.caption("先看图理解物理，再看公式，再回到工程设计。")

topic=st.radio("Choose a principle",["Why SJ lowers Ron","Charge imbalance","Dynamic incomplete ionization","Short-circuit hot spot","Process route"],horizontal=True)

if topic=="Why SJ lowers Ron":
    st.subheader("1 · Triangular field → rectangular-like field")
    x=np.linspace(0,1,200)
    tri=1-x
    rect=np.ones_like(x)*0.82
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=x,y=tri,name="Conventional drift: triangular E-field",fill="tozeroy"))
    fig.add_trace(go.Scatter(x=x,y=rect,name="Idealized SJ: flatter E-field",fill="tozeroy",opacity=.45))
    fig.update_layout(xaxis_title="Normalized drift depth",yaxis_title="Normalized electric field")
    st.plotly_chart(fig,use_container_width=True)
    causal_chain(["P/N lateral depletion","field reshaping","higher allowed N-column doping","lower drift resistance"])
    st.latex(r"Q_N=qN_DW_N\quad Q_P=qN_A^-W_P")
    st.latex(r"V_B\approx E_{C,z}L_{column}")
    takeaway("SJ 的关键不是“多一个 P 柱”，而是用横向耗尽重塑纵向电场，让漂移区可以更高掺杂。")
    why_it_matters("高压下 Rdrift 越重要，SJ 的结构价值越明显。")
    evidence_badge("model")

elif topic=="Charge imbalance":
    st.subheader("2 · Why a small process error matters")
    ar=st.slider("Aspect ratio L/W",2.,30.,10.,.5)
    delta=np.linspace(-.2,.2,201)
    score=1/(1+np.abs(delta)*ar)
    fig=go.Figure(go.Scatter(x=delta*100,y=score*100))
    fig.add_vline(x=0,line_dash="dash")
    fig.update_layout(xaxis_title="Charge imbalance (%)",yaxis_title="Illustrative BV retention (%)")
    st.plotly_chart(fig,use_container_width=True)
    causal_chain(["Dose/CD variation","QP ≠ QN","residual space charge","field tilting","BV margin loss"])
    takeaway("柱越深、节距越窄，制造误差越不能只看“±几%”，而要看它最终映射成多少 QP/QN 偏差。")
    st.warning("🟠 曲线是敏感度示意，不是经过标定的 BV 预测。")

elif topic=="Dynamic incomplete ionization":
    st.subheader("3 · Static balance can become transient imbalance")
    t=np.linspace(0,5,250)
    tau=st.slider("Illustrative ionization delay τ (µs)",0.05,3.,.8,.05)
    qp=1-np.exp(-t/tau)
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=t,y=qp,name="Illustrative P-column ionized charge"))
    fig.add_hline(y=1,line_dash="dash")
    fig.update_layout(xaxis_title="Time after transient (µs)",yaxis_title="Normalized effective P charge")
    st.plotly_chart(fig,use_container_width=True)
    causal_chain(["fast turn-off","acceptor ionization delay","temporary QP deficit","transient field redistribution","reverse-recovery / dynamic behavior"])
    takeaway("设计时不能只问室温静态 QP=QN，还要问开关瞬间 P 柱的有效电荷是否来得及建立。")
    evidence_badge("tutorial")
    st.warning("🟠 指数曲线和 τ 是教学模型；Tutorial 直接支持的是 delayed ionization 现象与暂态 charge imbalance。")

elif topic=="Short-circuit hot spot":
    st.subheader("4 · Why SJ can move the hot spot")
    z=np.linspace(0,1,200)
    e_u=np.exp(-5*z)
    e_s=np.exp(-((z-.55)/.25)**2)
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=z,y=e_u,name="UMOS illustrative field concentration"))
    fig.add_trace(go.Scatter(x=z,y=e_s,name="SJ illustrative deeper field peak"))
    fig.update_layout(xaxis_title="Normalized depth from surface",yaxis_title="Illustrative E-field / heat-source tendency")
    st.plotly_chart(fig,use_container_width=True)
    causal_chain(["SJ field redistribution","deeper E peak","J·E hot spot moves downward","surface Al sees less thermal stress","SC margin improves"])
    st.metric("Tutorial example tSC","15.0 µs SJ vs 13.0 µs UMOS")
    st.metric("ESC advantage @175°C","+53% at comparison point")
    takeaway("短路优势不只是 Ron 更低，而是“热在哪里产生”发生了变化。")
    evidence_badge("tutorial")

else:
    st.subheader("5 · Process route intuition")
    depth=st.select_slider("Column depth / voltage tendency",options=["shallow / ~1.2 kV","medium","deeper / ~3.3 kV"],value="shallow / ~1.2 kV")
    st.markdown("""
**Multi-epi** → 重复外延/注入，深度增加时层数与节拍压力上升  
**TFE** → 先深槽，再外延填充；柱越深越值得关注填槽质量与方向控制  
**MeV implant** → 高能注入，关注 damage / activation / depth  
**Channeling** → 利用晶体沟道提高射程，节拍短，但晶轴对准成为关键
""")
    st.dataframe({
      "Route":["Multi-epi","TFE","MeV implant","Channeling"],
      "1.2 kV cycle time":[0.75,0.23,0.20,0.08],
      "3.3 kV cycle time":[1.50,0.29,0.45,0.21]
    },hide_index=True,use_container_width=True)
    takeaway("从 1.2 kV 到 3.3 kV，不只是结构变深；制造路线的相对优势也在重新排序。")
    evidence_badge("tutorial")
