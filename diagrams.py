"""Teaching figures for the SiC console.

Field shapes and cross-sections are schematic. Numeric markers are either
labeled literature anchors or numbers already taken from the ICSCRM abstracts.
"""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

NAVY = "#1e4e79"
GOLD = "#b08a2e"
INK = "#14161a"
PILLAR = "#c4a574"


def _frame(fig: go.Figure, title: str, height: int = 380) -> go.Figure:
    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.35)",
        font=dict(family="Songti SC, Noto Serif SC, Georgia, serif", color=INK, size=13),
        margin=dict(l=12, r=12, t=48, b=12),
        height=height,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    return fig


def sj_cross_section() -> go.Figure:
    fig = go.Figure()
    for i in range(6):
        fig.add_shape(
            type="rect",
            x0=i, x1=i + 0.94, y0=0, y1=10,
            fillcolor=NAVY if i % 2 == 0 else PILLAR,
            line=dict(color="white", width=1),
        )
        fig.add_annotation(
            x=i + 0.47, y=5, text="N" if i % 2 == 0 else "P",
            showarrow=False, font=dict(color="white", size=16),
        )
    fig.add_annotation(x=3, y=10.55, text="漂移区截面 · 柱宽和柱深都是示意", showarrow=False, font=dict(size=12, color="#6d727b"))
    fig.update_xaxes(visible=False, range=[-0.15, 6.1])
    fig.update_yaxes(title="深度方向", range=[-0.2, 11.3], showgrid=False)
    return _frame(fig, "超结：交替 P/N 柱", 340)


def sj_field(imbalance_pct: float) -> go.Figure:
    """Normalized field. 0% is flat; imbalance tilts it. Not a TCAD solve."""
    y = np.linspace(0, 1, 120)
    slope = imbalance_pct / 100.0
    e_sj = np.clip(1.0 + slope * (2 * y - 1), 0, None)
    e_tri = 2 * (1 - y)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=y, y=e_tri, name="非超结 · 三角形", line=dict(color="#8a8175", dash="dash", width=2)))
    fig.add_trace(go.Scatter(x=y, y=e_sj, name="超结 · 随 ΔQ 倾斜", line=dict(color=NAVY, width=3)))
    fig.add_hline(y=1, line_dash="dot", line_color=GOLD, annotation_text="示意临界场", annotation_position="top left")
    fig.update_xaxes(title="归一化柱深  0 = 结  →  1 = 柱底")
    fig.update_yaxes(title="E / E_flat")
    return _frame(fig, f"电场形状 · 电荷失衡 {imbalance_pct:+.0f}%", 380)


def ionization_anchor() -> go.Figure:
    """Two published points for Al at 1e17 cm-3, EA ≈ 200 meV. Not interpolated as a device model."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[25, 300], y=[15, 75],
        mode="markers+text",
        text=["约 15%", "约 75%"],
        textposition="top center",
        marker=dict(size=14, color=NAVY),
        name="1×10¹⁷ cm⁻³ 例子",
    ))
    fig.update_xaxes(title="温度 (°C)", range=[0, 340])
    fig.update_yaxes(title="电离比例 (%)", range=[0, 100])
    return _frame(fig, "铝受主电离 · 文献中的一个例子", 320)


def trench_corner() -> go.Figure:
    fig = go.Figure()
    fig.add_shape(type="rect", x0=0, x1=10, y0=0, y1=8, fillcolor="#d9e2ec", line=dict(color=NAVY, width=1))
    fig.add_shape(type="rect", x0=3.2, x1=6.8, y0=3.2, y1=8.2, fillcolor="#f7f4ee", line=dict(color=NAVY, width=2))
    fig.add_shape(type="rect", x0=3.55, x1=6.45, y0=3.7, y1=8.3, fillcolor="#e7e1d6", line=dict(width=0))
    fig.add_shape(type="circle", x0=2.85, x1=3.85, y0=2.85, y1=3.85, fillcolor="#8f1d0c", line=dict(width=0), opacity=0.85)
    fig.add_shape(type="circle", x0=6.15, x1=7.15, y0=2.85, y1=3.85, fillcolor="#8f1d0c", line=dict(width=0), opacity=0.85)
    fig.add_annotation(x=5, y=6.2, text="栅", showarrow=False)
    fig.add_annotation(x=1.5, y=5.2, text="p 体", showarrow=False, font=dict(color=NAVY))
    fig.add_annotation(x=1.6, y=1.4, text="n− 漂移", showarrow=False, font=dict(color=NAVY))
    fig.add_annotation(x=3.3, y=2.3, text="角", showarrow=False, font=dict(color="#8f1d0c", size=12))
    fig.update_xaxes(visible=False, range=[-0.2, 10.2])
    fig.update_yaxes(visible=False, range=[-0.2, 8.8], scaleanchor="x", scaleratio=1)
    return _frame(fig, "沟槽角：电场在底部拐角集中", 380)


def mobility_split(trapped_fraction: float) -> go.Figure:
    trapped = float(np.clip(trapped_fraction, 0, 0.95))
    free = 1 - trapped
    fig = go.Figure()
    fig.add_trace(go.Bar(x=["反型层电子"], y=[free], name="自由 n_free", marker_color=NAVY))
    fig.add_trace(go.Bar(x=["反型层电子"], y=[trapped], name="被陷 n_trap", marker_color=GOLD))
    fig.update_layout(barmode="stack", yaxis_title="相对密度")
    fig.update_yaxes(range=[0, 1])
    return _frame(fig, f"μ 比例 ≈ {free:.2f}    （n_free / 总密度）", 320)


def bpd_schematic(mode: str) -> go.Figure:
    fig = go.Figure()
    bands = [
        (0, 3.2, "#8d8378", "n+ 衬底"),
        (3.2, 4.6, "#1e4e79", "高掺缓冲"),
        (4.6, 10, "#d5e0ea", "n− 漂移"),
    ]
    for y0, y1, color, label in bands:
        fig.add_shape(type="rect", x0=0, x1=10, y0=y0, y1=y1, fillcolor=color, line=dict(width=0), opacity=0.9)
        fig.add_annotation(x=8.3, y=(y0 + y1) / 2, text=label, showarrow=False, font=dict(color="white" if y1 < 4.6 else INK, size=12))
    if mode == "convert":
        fig.add_shape(type="line", x0=2.2, x1=4.0, y0=0.4, y1=3.2, line=dict(color="#f4e2b0", width=3))
        fig.add_shape(type="line", x0=4.0, x1=4.0, y0=3.2, y1=9.4, line=dict(color="#f4e2b0", width=3))
        fig.add_annotation(x=2.2, y=1.5, text="BPD", showarrow=False, font=dict(color="#fff8e8", size=12))
        fig.add_annotation(x=4.45, y=7.2, text="TED", showarrow=False, font=dict(color=NAVY, size=12))
        title = "外延界面附近：BPD 转成 TED"
    else:
        fig.add_shape(type="line", x0=1.5, x1=6.5, y0=1.0, y1=6.2, line=dict(color="#8f1d0c", width=4))
        fig.add_annotation(x=6.7, y=6.4, text="层错沿基面扩", showarrow=False, font=dict(color="#8f1d0c", size=12))
        fig.add_annotation(x=5.2, y=8.4, text="空穴到达衬底", showarrow=False, font=dict(color=NAVY, size=12))
        title = "复合增强滑移：单肖克莱层错扩张"
    fig.update_xaxes(visible=False, range=[-0.2, 10.2])
    fig.update_yaxes(visible=False, range=[-0.2, 10.4])
    return _frame(fig, title, 420)


def lifetime_bars() -> go.Figure:
    fig = go.Figure(go.Bar(
        x=["初始", "消除空位后", "再加表面钝化"],
        y=[1.8, 28.1, 34.2],
        marker_color=[ "#8a8175", NAVY, "#2f6f4e"],
        text=["1.8 μs", "28.1 μs", "34.2 μs"],
        textposition="outside",
    ))
    fig.update_yaxes(title="少子寿命 (μs)", range=[0, 42])
    return _frame(fig, "教程例子：碳空位消除后的寿命", 340)


def knowledge_stack() -> go.Figure:
    layers = [
        "材料", "晶体 / 外延", "缺陷", "工艺", "MOS 界面",
        "器件", "可靠性", "模块", "系统",
    ]
    fig = go.Figure()
    for i, name in enumerate(layers):
        y = len(layers) - i
        fig.add_shape(
            type="rect", x0=0.4, x1=6.6, y0=y - 0.38, y1=y + 0.38,
            fillcolor="rgba(30,78,121,0.10)" if i % 2 == 0 else "rgba(196,165,116,0.28)",
            line=dict(color=NAVY, width=1),
        )
        fig.add_annotation(x=3.5, y=y, text=f"{i+1}  {name}", showarrow=False, font=dict(size=14))
        if i < len(layers) - 1:
            fig.add_annotation(x=7.15, y=y - 0.5, text="↓", showarrow=False, font=dict(size=16, color=NAVY))
    fig.update_xaxes(visible=False, range=[0, 8])
    fig.update_yaxes(visible=False, range=[0.2, len(layers) + 0.8])
    return _frame(fig, "九层：上一层的工艺决定下一层能不能用", 520)
