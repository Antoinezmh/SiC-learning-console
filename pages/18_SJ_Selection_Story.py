import streamlit as st
st.title("🧩 How to Choose an SJ Process Route")
st.caption("把选型逻辑讲清楚，而不是让雷达图替你做决定。")

st.markdown("""
### Step 1 · 先问柱要做多深
柱深决定了 Multi-epi 的重复层数、implant 的能量/次数，以及 TFE 的 trench aspect ratio。

**Column depth ↑ → repeated modules / implant depth pressure ↑ → TFE relative attractiveness can increase**

### Step 2 · 再把 Cycle Time 和 Cost 分开
**Cycle time ≠ Cost.**  
工时短不代表设备便宜，也不代表折旧、维护、产能、良率后的 Cost/wafer 更低。

### Step 3 · 找每条路线真正的“杀手变量”
- **Multi-epi**：重复次数与累计均匀性
- **TFE**：trench geometry / crystal direction / void / fill morphology
- **MeV**：implant damage / activation / depth
- **Channeling**：crystal-axis alignment / range uniformity

### Step 4 · 最后才看器件收益
Ron(T)、Qrr、SC、Avalanche、bipolar degradation 是**结构 + 工艺 + lifetime + termination**共同结果，不能简单归功于“某一种制造路线”。

### Step 5 · Productization Gate
真正进入产品前，应把问题改写成：

> **哪条路线在目标 BV 下，能以可接受的 tool set、process window、wafer uniformity 和 yield，稳定实现所需的 SJ charge balance 与 ruggedness？**
""")
st.success("这就是 Comparator 的核心：不是找“理论冠军”，而是找在你的 fab 条件下最稳健的可制造方案。")
