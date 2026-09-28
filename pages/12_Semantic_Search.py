from pathlib import Path

import streamlit as st

from sic_ui import hero, inject_styles, section

ROOT = Path(__file__).resolve().parents[1]
CHROMA = ROOT / "data" / "chroma"
MANIFEST = ROOT / "data" / "vector_manifest.json"
COLLECTION = "sic_corpus"
MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

inject_styles()
hero(
    "Lookup",
    "文献查阅",
    "在已经入库的模块总结、摘要正文、工艺卡和原理说明里定位原句。中文词可以命中英文摘要。",
)

if not CHROMA.exists():
    st.error("还没有向量库。在仓库根目录运行 python3 scripts/embed_sic.py")
    st.stop()

import json

manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}


@st.cache_resource(show_spinner="加载向量模型和索引…")
def load_search():
    import chromadb
    from fastembed import TextEmbedding

    client = chromadb.PersistentClient(path=str(CHROMA))
    collection = client.get_collection(COLLECTION)
    model = TextEmbedding(manifest.get("model") or MODEL)
    return collection, model


collection, model = load_search()
kinds = manifest.get("kinds") or {}
c1, c2, c3, c4 = st.columns(4)
c1.metric("向量条数", f"{collection.count()}")
c2.metric("摘要块", kinds.get("abstract", "—"))
c3.metric("论文摘要卡", kinds.get("brief", "—"))
c4.metric("工艺卡 + 原理", (kinds.get("process_card") or 0) + (kinds.get("principle") or 0))
st.caption(f"模型 {manifest.get('model', MODEL)} · 余弦距离 · 索引在本机 data/chroma")

query = st.text_input("查找", placeholder="例如：1200°C H2/Ar、沟槽填充柱深、Fr-1B-02")
kind_filter = st.multiselect(
    "只在这些层里找",
    ["process_board", "summary", "abstract", "brief", "process_card", "principle"],
    default=[],
    format_func=lambda k: {
        "process_board": "工艺看板",
        "summary": "模块总结",
        "abstract": "摘要正文",
        "brief": "论文工艺摘要",
        "process_card": "核对工艺卡",
        "principle": "原理说明",
    }[k],
)
top_k = st.slider("条数", 3, 12, 6)

if query.strip():
    vector = next(model.embed([query.strip()])).tolist()
    where = {"kind": {"$in": kind_filter}} if kind_filter else None
    found = collection.query(query_embeddings=[vector], n_results=top_k, where=where)
    section("结果", "nearest")
    docs = found["documents"][0]
    metas = found["metadatas"][0]
    dists = found["distances"][0]
    if not docs:
        st.info("这个筛选下没有结果。")
    for i, (doc, meta, dist) in enumerate(zip(docs, metas, dists), 1):
        score = 1 - dist
        with st.container(border=True):
            head, val = st.columns([4, 1])
            title = meta.get("title") or meta.get("paper_id") or "未命名"
            with head:
                st.markdown(f"**{i}. {title}**")
                bits = [meta.get("kind") or "", meta.get("paper_id") or "", meta.get("module") or "", meta.get("day") or ""]
                st.caption(" · ".join(bit for bit in bits if bit))
            with val:
                st.metric("相近度", f"{score:.2f}")
            st.write(doc[:700] + ("…" if len(doc) > 700 else ""))
            pid = meta.get("paper_id") or ""
            links = []
            if meta.get("kind") == "summary":
                links.append("[打开会议总结](/Synthesis)")
            if meta.get("kind") == "process_board":
                links.append("[打开工艺看板](/Process_Board)")
            if pid:
                links.append(f"[在工艺数据库打开 {pid}](/Abstract_Atlas?paper={pid})")
            if links:
                st.markdown("　".join(links))
else:
    section("库里的层")
    st.markdown(
        "工艺看板、模块总结、摘要正文、论文工艺摘要、核对工艺卡、原理说明。"
        "查到的条目链回工艺数据库里的原摘要。"
    )
