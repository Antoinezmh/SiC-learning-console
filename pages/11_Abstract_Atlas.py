import pandas as pd
import plotly.express as px
import streamlit as st

from sic_ui import hero, inject_styles, section
from sicdb import KIND_LABEL, MODULE_LABEL, load_abstracts, load_cards, load_catalog, load_facts, load_signals

inject_styles()

hero(
    "ICSCRM 2026",
    "工艺数据库",
    "紫色数字是从摘要正文抽出的提及，带上下文。绿色工艺卡是核对过的步骤。原理图在超结、MOS 和缺陷这三页。",
)

catalog = load_catalog()
facts = load_facts()
signals = load_signals()
cards = load_cards()
if not catalog or not facts:
    st.error("数据库还没建完。先运行 scripts/build_icscrm_catalog.py 和 scripts/extract_abstract_signals.py")
    st.stop()


@st.cache_data(show_spinner=False)
def abstracts() -> dict:
    return load_abstracts()


cat = pd.DataFrame(catalog)
fact = pd.DataFrame(facts)
sig = pd.DataFrame(signals)
card_df = pd.DataFrame(cards) if cards else pd.DataFrame(columns=["source_id"])

cat = cat.merge(
    fact[["id", "pdf_page", "gases", "temp_min", "temp_max", "n_signals", "process_sentences", "text_modules", "n_chars"]],
    on="id",
    how="left",
)
cat["n_signals"] = cat["n_signals"].fillna(0).astype(int)
cat["module_label"] = cat["primary_module"].map(MODULE_LABEL).fillna(cat["primary_module"])
cat["gases"] = cat["gases"].apply(lambda v: v if isinstance(v, list) else [])
cat["process_sentences"] = cat["process_sentences"].apply(lambda v: v if isinstance(v, list) else [])
cat["where"] = cat.apply(lambda r: r["session"] or r["track"] or r["kind"], axis=1)

id_module = cat.set_index("id")["module_label"]
id_title = cat.set_index("id")["title"]
sig["module_label"] = sig["id"].map(id_module).fillna("未入目录")
sig["title"] = sig["id"].map(id_title).fillna("")
sig["kind_label"] = sig["kind"].map(KIND_LABEL).fillna(sig["kind"])
sig["reading"] = sig.apply(
    lambda r: f"{r['value']:g}" + (f"–{r['value_hi']:g}" if pd.notna(r["value_hi"]) else "") + f" {r['unit']}",
    axis=1,
)

gas_options = sorted({g for gases in cat["gases"] for g in gases})

with st.sidebar:
    st.header("筛选")
    query = st.text_input("题目 / 作者 / 编号 / 正文句子")
    modules = st.multiselect("主模块", sorted(cat["module_label"].dropna().unique()))
    kind = st.selectbox("参数", list(KIND_LABEL), index=0, format_func=lambda k: KIND_LABEL[k])
    gases = st.multiselect("气氛 / 前驱体", gas_options)
    process_only = st.checkbox("只看工艺模块", value=True)
    with_numbers = st.checkbox("只看正文里抽出了数字的", value=False)

view = cat
if process_only:
    view = view[view["process_relevant"]]
if modules:
    view = view[view["module_label"].isin(modules)]
if gases:
    view = view[view["gases"].apply(lambda gs: bool(set(gs) & set(gases)))]
if with_numbers:
    view = view[view["n_signals"] > 0]
if query:
    q = query.lower()
    sent_hit = view["process_sentences"].apply(lambda xs: any(q in s.lower() for s in xs))
    view = view[
        view["title"].str.lower().str.contains(q, na=False)
        | view["authors"].str.lower().str.contains(q, na=False)
        | view["id"].str.lower().str.contains(q, na=False)
        | sent_hit
    ]

sig_view = sig[sig["id"].isin(set(view["id"])) & (sig["kind"] == kind)].copy()

m1, m2, m3, m4 = st.columns(4)
m1.metric("当前论文", len(view))
m2.metric(f"{KIND_LABEL[kind]}提及", len(sig_view))
m3.metric("有正文", int(view["n_chars"].fillna(0).gt(0).sum()))
m4.metric("全库提及", len(sig))

tab_dist, tab_paper, tab_card = st.tabs(["参数分布", "论文", "核对过的工艺卡"])

with tab_dist:
    if sig_view.empty:
        st.info("这个筛选下没有这类数字。换一个参数，或放宽侧栏条件。")
    else:
        plot_df = sig_view.copy()
        plot_df["y"] = plot_df["value_hi"].fillna(plot_df["value"])
        log_y = kind in {"doping", "dose"}
        fig = px.strip(
            plot_df,
            x="module_label",
            y="y",
            color="unit",
            hover_data=["id", "reading", "context", "title"],
            title=f"{KIND_LABEL[kind]} · 按模块",
            labels={"y": KIND_LABEL[kind], "module_label": ""},
            log_y=log_y,
        )
        fig.update_layout(height=460, margin=dict(l=10, r=10, t=48, b=10))
        st.plotly_chart(fig, width="stretch")
        show_sig = sig_view[["id", "reading", "module_label", "context", "pdf_page"]].rename(
            columns={"id": "编号", "reading": "数值", "module_label": "模块", "context": "上下文", "pdf_page": "PDF页"}
        )
        picked = st.dataframe(
            show_sig,
            width="stretch",
            hide_index=True,
            height=320,
            on_select="rerun",
            selection_mode="single-row",
            column_config={"上下文": st.column_config.TextColumn(width="large")},
        )
        rows = picked.selection.rows if picked.selection else []
        if rows:
            hit = show_sig.iloc[rows[0]]
            st.session_state["paper"] = hit["编号"]
            st.markdown(f"**{hit['编号']}**  {id_title.get(hit['编号'], '')}")
            st.write(hit["上下文"])

    gas_rows = []
    for name in gas_options:
        gas_rows.append({"气体": name, "论文数": int(view["gases"].apply(lambda gs, n=name: n in gs).sum())})
    gas_df = pd.DataFrame(gas_rows)
    gas_df = gas_df[gas_df["论文数"] > 0].sort_values("论文数")
    if len(gas_df):
        fig_g = px.bar(gas_df, x="论文数", y="气体", orientation="h", title="当前筛选里提到的气氛 / 前驱体")
        fig_g.update_layout(height=380, margin=dict(l=10, r=10, t=48, b=10))
        st.plotly_chart(fig_g, width="stretch")

with tab_paper:
    options = view["id"].tolist()
    if not options:
        st.info("没有符合筛选的论文。")
    else:
        if st.session_state.get("paper") not in options:
            st.session_state["paper"] = "Mo-1A-01" if "Mo-1A-01" in options else options[0]
        choice = st.selectbox(
            "论文",
            options,
            key="paper",
            format_func=lambda i: f"{i}  {id_title.get(i, '')[:88]}",
        )
        row = view[view["id"] == choice].iloc[0]
        st.subheader(row["title"])
        st.write(row["authors"] or "")
        st.caption(f"{row['orgs'] or ''}  ·  {row['where']}  ·  PDF p.{row['pdf_page'] if pd.notna(row['pdf_page']) else row['program_page']}")
        if row["gases"]:
            st.write("气氛 / 前驱体：" + "、".join(row["gases"]))
        if pd.notna(row["temp_min"]):
            st.write(f"文中温度范围：{row['temp_min']:g}–{row['temp_max']:g} °C")

        left, right = st.columns([1.05, 1])
        with left:
            st.markdown("**工艺相关句子**")
            if row["process_sentences"]:
                for sent in row["process_sentences"]:
                    st.markdown(f"- {sent}")
            else:
                st.caption("没有抽到明显的工艺句。")
            mine = sig[sig["id"] == choice][["kind_label", "reading", "context"]].rename(
                columns={"kind_label": "参数", "reading": "数值", "context": "上下文"}
            )
            st.markdown("**抽出的数字**")
            if mine.empty:
                st.caption("这篇正文里没有匹配到数值模板。")
            else:
                st.dataframe(mine, width="stretch", hide_index=True, height=280)
            if len(card_df):
                hand = card_df[card_df["source_id"] == choice]
                if len(hand):
                    st.markdown("**核对过的工艺卡**")
                    st.dataframe(hand, width="stretch", hide_index=True)
        with right:
            body = abstracts().get(choice, {}).get("text", "")
            st.markdown("**摘要正文**")
            if body:
                st.text_area("abstract", body, height=640, label_visibility="collapsed")
            else:
                st.info("本地没有这篇的正文。plenary 和撤稿可能只有议程条目。")

with tab_card:
    st.caption("这些卡是对照摘要逐项核对过的。自动抽出的数字在上面两个标签里，不要和这里混成同一级证据。")
    if card_df.empty:
        st.info("没有工艺卡。")
    else:
        card_df = card_df.copy()
        card_df["模块"] = card_df["module"].map(MODULE_LABEL).fillna(card_df["module"])
        st.dataframe(
            card_df[["source_id", "模块", "route", "step", "name", "ambient", "claim", "evidence"]],
            width="stretch",
            hide_index=True,
            height=280,
        )
        options = sorted(card_df["source_id"].unique())
        pick = st.selectbox("看一条流程", options, index=options.index("Mo-1A-01") if "Mo-1A-01" in options else 0)
        steps = card_df[card_df["source_id"] == pick].sort_values(["route", "step"])
        for route, group in steps.groupby("route", sort=False):
            st.markdown(f"#### {route}")
            cols = st.columns(len(group))
            for col, (_, step) in zip(cols, group.iterrows()):
                temp = step.get("temperature_C")
                if isinstance(temp, (int, float)) and pd.notna(temp):
                    label = f"{temp:g} °C"
                elif isinstance(temp, str) and temp.strip():
                    label = temp
                else:
                    label = step.get("ambient") or step.get("chemistry") or "条件见说明"
                with col:
                    st.metric(f"{int(step['step'])}. {step['name']}", label)
                    st.write(step.get("claim") or "")
                    st.caption(step.get("evidence") or "")
