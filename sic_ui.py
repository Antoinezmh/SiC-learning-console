"""SiC console UI, adapted from the AIxResearch editorial workbench.

Paper ground, one navy accent, serif titles, hairline sections, and the
light glass sidebar used on that panel.
"""

from __future__ import annotations

import html

import streamlit as st

try:
    from streamlit.errors import StreamlitPageNotFoundError as _PageNotFoundErr
except ImportError:  # pragma: no cover
    class _PageNotFoundErr(Exception):
        pass

_CSS = """
<style>
  :root{
    --ink:#14161a; --paper:#faf9f7; --accent:#1e4e79; --accent-deep:#12395c;
    --line:#e3e1da; --muted:#6d727b;
  }
  html,body,[data-testid="stAppViewContainer"]{background:var(--paper);}
  [data-testid="stHeader"]{background:transparent !important;}
  body{color:var(--ink);}
  h1,h2,h3{font-family:"Songti SC","Noto Serif SC",Georgia,serif !important;letter-spacing:.01em;}
  .block-container{padding:1.6rem 1.2rem 3rem;max-width:1240px;}
  a{color:var(--accent);text-decoration:none;}
  a:hover{text-decoration:underline;}

  .pg-kicker{font-size:.72rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;
    color:var(--muted);border-top:2px solid var(--ink);display:inline-block;padding-top:.5rem;margin:0 0 .8rem;}
  .pg-hero{position:relative;overflow:hidden;padding:26px 28px 22px;margin:0 0 16px;border-radius:28px;
    border:1px solid rgba(255,255,255,.72);
    background:
      radial-gradient(circle at 20% 12%, rgba(255,255,255,.94), rgba(255,255,255,.34) 30%, transparent 55%),
      radial-gradient(circle at 86% 18%, rgba(30,78,121,.16), transparent 34%),
      linear-gradient(135deg, rgba(255,255,255,.78), rgba(232,239,246,.48));
    box-shadow:inset 0 1px 0 rgba(255,255,255,.95), 0 22px 55px rgba(30,78,121,.10);}
  .pg-hero-title{font-family:"Songti SC","Noto Serif SC",Georgia,serif;
    font-size:clamp(28px,3.6vw,40px);line-height:1.15;font-weight:700;margin:0 0 .45rem;color:var(--ink);}
  .pg-hero-sub{color:var(--muted);font-size:.96rem;margin:0 0 .7rem;max-width:78ch;line-height:1.55;}
  .pg-meta{font-size:.8rem;color:var(--muted);letter-spacing:.04em;}
  .pg-meta b{color:var(--ink);font-weight:600;}

  .pg-section{display:flex;align-items:baseline;gap:.7rem;margin:1.5rem 0 .75rem;}
  .pg-section .t{font-family:"Songti SC","Noto Serif SC",Georgia,serif;font-size:1.22rem;font-weight:700;}
  .pg-section .n{font-size:.7rem;color:var(--muted);letter-spacing:.16em;text-transform:uppercase;}
  .pg-section::after{content:"";flex:1;border-top:1px solid var(--line);transform:translateY(-4px);}

  [data-testid="stMetric"]{
    background:radial-gradient(circle at 22% 12%, rgba(255,255,255,.95), rgba(255,255,255,.45) 46%, transparent 70%),
      linear-gradient(145deg, rgba(255,255,255,.8), rgba(255,255,255,.42)) !important;
    border:1px solid rgba(255,255,255,.7) !important;border-radius:18px !important;
    padding:14px 16px !important;
    box-shadow:inset 0 1px 0 rgba(255,255,255,.92), 0 12px 28px rgba(27,37,52,.06) !important;}
  [data-testid="stMetricLabel"] p,[data-testid="stMetricLabel"]{font-size:.7rem !important;
    letter-spacing:.12em;text-transform:uppercase;color:var(--muted) !important;font-weight:600;}
  [data-testid="stMetricValue"]{font-family:"Songti SC","Noto Serif SC",Georgia,serif;font-weight:700;color:var(--ink);}

  .stButton>button,.stDownloadButton>button,.stLinkButton>button{
    border-radius:16px !important;border:1px solid rgba(255,255,255,.75) !important;
    background:linear-gradient(145deg, rgba(255,255,255,.9), rgba(255,255,255,.5)) !important;
    color:var(--ink) !important;font-weight:600;box-shadow:inset 0 1px 0 #fff, 0 8px 18px rgba(27,37,52,.06) !important;}
  .stButton>button:hover{border-color:rgba(30,78,121,.35) !important;color:var(--accent) !important;}
  .stButton>button[kind="primary"]{
    background:var(--accent) !important;border-color:var(--accent) !important;color:#fff !important;}

  section[data-testid="stSidebar"]{
    background:
      radial-gradient(circle at 12% 6%, rgba(255,255,255,.95), transparent 42%),
      radial-gradient(circle at 88% 18%, rgba(30,78,121,.12), transparent 46%),
      linear-gradient(175deg, rgba(255,255,255,.78), rgba(244,241,235,.62)) !important;
    border-right:1px solid rgba(255,255,255,.72) !important;}
  [data-testid="stSidebarNavLink"], [data-testid="stSidebarNav"] li a, [data-testid="stSidebarNavItems"] a{
    margin:.18rem .2rem !important;padding:.58rem .9rem !important;border-radius:18px !important;
    border:1px solid rgba(255,255,255,.72) !important;
    background:linear-gradient(145deg, rgba(255,255,255,.86), rgba(255,255,255,.42)) !important;
    box-shadow:inset 0 1px 0 #fff, 0 8px 16px rgba(27,37,52,.05) !important;
    color:var(--ink) !important;font-weight:600 !important;text-decoration:none !important;}
  [data-testid="stSidebarNavLink"][aria-current="page"],
  [data-testid="stSidebarNav"] li a[aria-current="page"]{
    background:linear-gradient(135deg, rgba(30,78,121,.16), rgba(176,138,46,.10)) !important;
    border-color:rgba(30,78,121,.35) !important;color:var(--accent-deep) !important;}

  .pg-chip{display:inline-block;border:1px solid var(--line);background:#fff;border-radius:2px;
    padding:.12em .6em;font-size:.78rem;color:var(--ink);margin:0 .35rem .35rem 0;}
  .pg-badge{display:inline-block;border-radius:2px;padding:.08em .5em;font-size:.72rem;font-weight:700;letter-spacing:.06em;}
  .pg-badge.ok{background:#e4efe6;color:#1f5c2e;border:1px solid #b4d3ba;}
  .pg-badge.info{background:#e8eef5;color:#1e4e79;border:1px solid #bfd0e0;}
  .pg-badge.yellow{background:#f7efda;color:#77591a;border:1px solid #e0cb96;}
  .pg-badge.gray{background:#efede8;color:#55595f;border:1px solid var(--line);}

  [data-testid="stVerticalBlockBorderWrapper"]{border-color:rgba(255,255,255,.7) !important;border-radius:18px !important;
    background:linear-gradient(145deg, rgba(255,255,255,.78), rgba(255,255,255,.46));
    box-shadow:inset 0 1px 0 rgba(255,255,255,.9), 0 10px 24px rgba(27,37,52,.05);}
  .stTabs [data-baseweb="tab-list"]{gap:2px;border-bottom:1px solid var(--line);}
  .stTabs [aria-selected="true"]{color:var(--accent);border-bottom:2px solid var(--accent);}
  [data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:8px;}

  .kb-chart{display:flex;flex-direction:column;gap:.5rem;padding:.2rem 0 .4rem;}
  .kb-row{display:grid;grid-template-columns:9.2em 1fr 2.4em;align-items:center;gap:.6rem;}
  .kb-label{font-size:.82rem;color:var(--ink);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
  .kb-track{height:12px;background:#efede8;border-radius:2px;overflow:hidden;}
  .kb-bar{display:block;height:100%;background:#1e4e79;}
  .kb-count{font-size:.82rem;font-weight:700;text-align:right;font-variant-numeric:tabular-nums;}

  header[data-testid="stHeader"] [data-testid="stToolbar"],
  header[data-testid="stHeader"] [data-testid="stDecoration"]{display:none;}
  [data-testid="stAppViewContainer"]{
    background:
      radial-gradient(circle at 12% 0%, rgba(30,78,121,.08), transparent 34%),
      radial-gradient(circle at 88% 8%, rgba(176,138,46,.08), transparent 32%),
      linear-gradient(160deg, #fbfaf7 0%, #f3f0ea 100%) !important;}
</style>
"""


def inject_styles() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def hero(kick: str, title: str, subtitle: str = "", meta_html: str = "") -> None:
    parts = [
        f'<div class="pg-kicker">{html.escape(kick)}</div>',
        f'<div class="pg-hero-title">{html.escape(title)}</div>',
    ]
    if subtitle:
        parts.append(f'<p class="pg-hero-sub">{html.escape(subtitle)}</p>')
    if meta_html:
        parts.append(f'<div class="pg-meta">{meta_html}</div>')
    st.markdown(f'<div class="pg-hero">{"".join(parts)}</div>', unsafe_allow_html=True)


def section(title: str, note: str = "") -> None:
    note_html = f'<span class="n">{html.escape(note)}</span>' if note else ""
    st.markdown(
        f'<div class="pg-section"><span class="t">{html.escape(title)}</span>{note_html}</div>',
        unsafe_allow_html=True,
    )


def chip(text: str) -> str:
    return f'<span class="pg-chip">{html.escape(text)}</span>'


def badge(level: str, label: str) -> str:
    return f'<span class="pg-badge {html.escape(level)}">{html.escape(label)}</span>'


def bars(rows: list[tuple[str, int]]) -> None:
    peak = max((n for _, n in rows), default=1) or 1
    body = "".join(
        f'<div class="kb-row"><span class="kb-label">{html.escape(label)}</span>'
        f'<span class="kb-track"><span class="kb-bar" style="width:{100 * n / peak:.0f}%"></span></span>'
        f'<span class="kb-count">{n}</span></div>'
        for label, n in rows
    )
    st.markdown(f'<div class="kb-chart">{body}</div>', unsafe_allow_html=True)


def page_link(path: str, label: str, icon: str | None = None) -> None:
    try:
        st.page_link(path, label=label, icon=icon)
    except (KeyError, _PageNotFoundErr):
        st.caption(label)
