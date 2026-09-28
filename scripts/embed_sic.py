"""Embed the SiC console corpus into a local Chroma collection.

Sources: abstract bodies, one structured brief per paper, parameter mentions,
checked process cards, and the principle notes shown in the console.
Model: paraphrase-multilingual-MiniLM-L12-v2 so a Chinese query can hit English abstracts.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CHROMA = DATA / "chroma"
COLLECTION = "sic_corpus"
MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

PRINCIPLES = [
    {
        "id": "principle-sj-field",
        "title": "超结电荷平衡与电场",
        "text": (
            "SiC superjunction charge balance. Alternating P and N pillars reshape the drift electric field "
            "from a triangle into a flatter profile, so the drift can be doped higher and Ron,sp falls. "
            "QN = q ND WN, QP = q NA- WP. Effective ionized acceptor density matters, not the nominal Al dose. "
            "电荷失衡会把电场向柱的一端倾斜。教学示意图，不是 TCAD。"
        ),
    },
    {
        "id": "principle-al-ionization",
        "title": "铝受主不完全电离",
        "text": (
            "4H-SiC aluminum acceptor ionization energy is about 197.9 meV on the hexagonal Si site and "
            "201.3 meV on the cubic site. At 1e17 cm-3 and 200 meV, roughly 15% of acceptors are ionized "
            "at room temperature and about 75% at 300 C. MeV Al implants used for superjunction pillars "
            "have been reported with an effective ionization energy near 330 meV. "
            "室温配平的 p 柱到 175–200°C 不一定仍然配平。"
        ),
    },
    {
        "id": "principle-sj-routes",
        "title": "超结造柱：沟道注入与沟槽填充",
        "text": (
            "Dopants hardly diffuse in 4H-SiC, so deep pillars are made by channeling or high-energy implantation "
            "or by trench etch plus epitaxial refill. ICSCRM Fr-1B-02: 1200 V pillars about 5–8 um at "
            "1e16–1e17 cm-3, Al up to 12 MeV and P up to 14 MeV along [0001]. "
            "ICSCRM We-3B-02: SiH4:C3H8:H2 + TMA + HCl, fill up to 10 um/h and trenches about 50 um; "
            "a partial SJ MOSFET about 7.8 kV and 17.8 mohm cm2 with 25 um pillars. "
            "Al incorporates more on (0001) than on sidewalls. "
            "Published multi-epi channeling: about 4.9 um and 1000 V in two epi steps; conventional high-energy "
            "implants about 3.7 um and 800 V in three steps. Chlorinated trench fill at 1550 C has been "
            "reported at about 19 um/h for 3 um wide trenches."
        ),
    },
    {
        "id": "principle-mos",
        "title": "MOS 自由电荷、沟槽角",
        "text": (
            "Channel mobility is limited by the free-carrier fraction: mu_ch ≈ mu_free * n_free / (n_free + n_trap). "
            "Split C-V and MOS-Hall separate free and trapped charge. "
            "Trench corners crowd the oxide field. ICSCRM Tu-3A-02: Ar anneal rounds the top corner to about "
            "138 nm, H2 anneal to about 80 nm, and both reduce IGSS at VGS = 22 V. "
            "Ron = Rch + Racc + RJFET + Rdrift + Rsub + Rcontact."
        ),
    },
    {
        "id": "principle-bpd",
        "title": "BPD、层错与双极退化",
        "text": (
            "Basal plane dislocations plus minority-carrier recombination drive single Shockley stacking-fault "
            "expansion and on-state degradation. Epitaxy can convert BPDs to threading edge dislocations near "
            "the substrate interface because they can share a Burgers vector. "
            "A heavily doped n+ buffer increases recombination and keeps holes from reaching substrate BPDs. "
            "Z1/2 is the carbon vacancy. Tutorial lifetime example: about 1.8 us, then 28.1 us after vacancy "
            "elimination, then 34.2 us after surface passivation."
        ),
    },
    {
        "id": "principle-stack",
        "title": "九层知识链",
        "text": (
            "Material, crystal and epitaxy, defects, process, MOS interface, device, reliability, module, system. "
            "PVT bulk growth, step-flow epitaxy, implantation, oxidation, anneal, trench, superjunction. "
            "Reliability covers BTI, gate oxide, bipolar degradation, short circuit and avalanche."
        ),
    },
]


def load_jsonl(name: str) -> list[dict]:
    path = DATA / name
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def clip_program_bleed(text: str) -> str:
    for marker in ("Detailed Poster Program", "Program at a Glance", "Oral Sessions ("):
        idx = text.find(marker)
        if idx > 800:
            text = text[:idx]
    return text


def chunks(text: str, size: int = 1000, overlap: int = 160) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    if len(text) <= size:
        return [text]
    step = size - overlap
    out = []
    start = 0
    while start < len(text):
        out.append(text[start : start + size])
        if start + size >= len(text):
            break
        start += step
    return out


def build_docs() -> list[dict]:
    catalog = {row["id"]: row for row in load_jsonl("catalog.jsonl")}
    facts = {row["id"]: row for row in load_jsonl("paper_facts.jsonl")}
    signals: dict[str, list[dict]] = {}
    for row in load_jsonl("signals.jsonl"):
        signals.setdefault(row["id"], []).append(row)
    docs: list[dict] = []

    for row in load_jsonl("abstracts.jsonl"):
        pid = row["id"]
        meta = catalog.get(pid, {})
        fact = facts.get(pid, {})
        title = meta.get("title") or pid
        header = f"{pid} {title}\n{meta.get('authors', '')}\n{meta.get('session') or meta.get('track') or ''}"
        body = clip_program_bleed(row.get("text") or "")
        for i, piece in enumerate(chunks(body)):
            docs.append({
                "uid": f"{pid}#a{i}",
                "kind": "abstract",
                "paper_id": pid,
                "title": title[:240],
                "day": meta.get("day") or "",
                "module": meta.get("primary_module") or "",
                "text": f"{header}\n{piece}",
            })
        sentences = fact.get("process_sentences") or []
        gases = ", ".join(fact.get("gases") or [])
        sig_lines = []
        for sig in signals.get(pid, [])[:16]:
            hi = sig.get("value_hi")
            span = f"{sig['value']:g}" + (f"–{hi:g}" if hi else "")
            sig_lines.append(f"{sig['kind']} {span} {sig['unit']}: {sig['context']}")
        brief = "\n".join([
            header,
            f"modules: {', '.join(meta.get('modules') or [])}",
            f"gases: {gases}",
            f"temperature: {fact.get('temp_min')}–{fact.get('temp_max')} °C" if fact.get("temp_min") else "",
            *sentences,
            *sig_lines,
        ])
        brief = re.sub(r"\n{2,}", "\n", brief).strip()
        if len(brief) > 80:
            docs.append({
                "uid": f"{pid}#brief",
                "kind": "brief",
                "paper_id": pid,
                "title": title[:240],
                "day": meta.get("day") or "",
                "module": meta.get("primary_module") or "",
                "text": brief[:4000],
            })

    for card in load_jsonl("process_cards.jsonl"):
        text = " ".join(
            str(card.get(key) or "")
            for key in ("source_id", "module", "route", "name", "ambient", "chemistry", "claim", "evidence", "metric", "value", "unit")
        )
        docs.append({
            "uid": f"card:{card.get('card_id')}",
            "kind": "process_card",
            "paper_id": card.get("source_id") or "",
            "title": card.get("name") or card.get("card_id") or "",
            "day": "",
            "module": card.get("module") or "",
            "text": text,
        })

    for item in PRINCIPLES:
        docs.append({
            "uid": item["id"],
            "kind": "principle",
            "paper_id": "",
            "title": item["title"],
            "day": "",
            "module": "",
            "text": item["text"],
        })
    summary_path = DATA / "summaries.json"
    summaries = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.exists() else []
    for item in summaries:
        papers = []
        for point in item.get("points") or []:
            papers.extend(point.get("papers") or [])
        body = item.get("lead", "") + "\n" + "\n".join(point.get("text", "") for point in item.get("points") or [])
        docs.append({
            "uid": f"summary:{item['id']}",
            "kind": "summary",
            "paper_id": papers[0] if papers else "",
            "title": item.get("title") or item["id"],
            "day": "",
            "module": item.get("module") or "",
            "text": body,
        })
    board_path = DATA / "process_board.json"
    if board_path.exists():
        board = json.loads(board_path.read_text(encoding="utf-8"))
        for route in board.get("routes") or []:
            docs.append({
                "uid": f"board:{route['id']}",
                "kind": "process_board",
                "paper_id": "",
                "title": route.get("title") or route["id"],
                "day": "",
                "module": "gate_stack",
                "text": " ".join(route.get(k) or "" for k in ("title", "steps", "why", "limit")),
            })
        for cond in board.get("conditions") or []:
            bits = [cond.get("title") or "", cond.get("verdict") or "", cond.get("mechanism") or ""]
            papers = []
            for row in cond.get("rows") or []:
                bits.append(row.get("condition") or "")
                bits.append(row.get("result") or "")
                papers.extend(row.get("papers") or [])
            docs.append({
                "uid": f"board:{cond['id']}",
                "kind": "process_board",
                "paper_id": papers[0] if papers else "",
                "title": cond.get("title") or cond["id"],
                "day": "",
                "module": "gate_stack",
                "text": "\n".join(bits),
            })
    return docs


def main() -> None:
    docs = build_docs()
    if not docs:
        raise SystemExit("No documents to embed. Build the catalog and abstracts first.")
    print(f"documents {len(docs)}", flush=True)
    from fastembed import TextEmbedding

    model = TextEmbedding(MODEL)
    vectors = list(model.embed(doc["text"] for doc in docs))

    import chromadb

    CHROMA.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA))
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass
    coll = client.create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})
    batch = 256
    for start in range(0, len(docs), batch):
        part = docs[start : start + batch]
        vec = vectors[start : start + batch]
        coll.add(
            ids=[doc["uid"] for doc in part],
            documents=[doc["text"] for doc in part],
            embeddings=[v.tolist() for v in vec],
            metadatas=[{
                "kind": doc["kind"],
                "paper_id": doc["paper_id"],
                "title": doc["title"],
                "day": doc["day"],
                "module": doc["module"],
            } for doc in part],
        )
        print(f"added {start + len(part)}/{len(docs)}", flush=True)
    manifest = {
        "model": MODEL,
        "collection": COLLECTION,
        "count": coll.count(),
        "kinds": {},
    }
    for doc in docs:
        manifest["kinds"][doc["kind"]] = manifest["kinds"].get(doc["kind"], 0) + 1
    (DATA / "vector_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False))
    # ONNX runtime can abort while the interpreter is shutting down after a successful write.
    import os
    os._exit(0)


if __name__ == "__main__":
    main()
