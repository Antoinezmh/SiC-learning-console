"""Pull process parameters out of the ICSCRM 2026 abstract bodies.

Writes:
  data/abstracts.jsonl   full cleaned text (local; gitignored)
  data/paper_facts.jsonl per-paper gases, ranges, process sentences
  data/signals.jsonl     one row per numeric mention, with a short context
"""

from __future__ import annotations

import json
import re
import warnings
from collections import defaultdict
from pathlib import Path

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "References" / "ICSCRM2026_AbstractBook23_092526.pdf"
DATA = ROOT / "data"

ID = (
    r"(?:(?:Mo|Tu|We|Th|Fr)-(?:P|PL|[123][AB])-\d{2}(?:LN)?"
    r"|(?:Mo|Tu|We|Th|Fr)-IP|IP-\d{2})"
)
HEADER = re.compile(rf"({ID})(?:\s*/\s*({ID}))?\s*\|\s*Abstract", re.I)

MODULE_RULES = [
    ("sj", re.compile(r"super[\s-]?junction|\bpillars?\b", re.I)),
    ("trench", re.compile(r"\btrench\b|corner radius|corner round", re.I)),
    ("implant", re.compile(r"implant|channeling|dopant activation", re.I)),
    ("gate_stack", re.compile(r"\bMOS\b|SiO2|nitrid|gate dielectric|channel mobility|interface state", re.I)),
    ("epi", re.compile(r"epitax|epilayer|homoepitax|\bCVD\b", re.I)),
    ("bulk", re.compile(r"\bPVT\b|HTCVD|sublimation|solution growth|bulk crystal|boule", re.I)),
    ("contact", re.compile(r"schottky|ohmic contact|metalliz", re.I)),
    ("defect", re.compile(r"dislocation|stacking fault|\bBPD\b|micropipe|\bvacanc", re.I)),
    ("reliability", re.compile(r"reliab|\bBTI\b|short-circuit|bipolar degradation", re.I)),
    ("quantum", re.compile(r"quantum|qubit|color center", re.I)),
    ("device", re.compile(r"MOSFET|IGBT|\bJBS\b|JFET|FinFET|\bSBD\b", re.I)),
]

GAS_RULES = [
    ("H2", re.compile(r"\bH\s*2\b|hydrogen", re.I)),
    ("Ar", re.compile(r"\bAr(?:gon)?\b")),
    ("NO", re.compile(r"\bNO\b(?!\s*x)")),
    ("N2O", re.compile(r"\bN\s*2\s*O\b", re.I)),
    ("CO2", re.compile(r"\bCO\s*2\b", re.I)),
    ("HCl", re.compile(r"\bHCl\b")),
    ("SiH4", re.compile(r"\bSiH\s*4\b", re.I)),
    ("C3H8", re.compile(r"\bC\s*3\s*H\s*8\b", re.I)),
    ("TMA", re.compile(r"\bTMA\b|trimethylaluminum", re.I)),
    ("NH3", re.compile(r"\bNH\s*3\b", re.I)),
    ("N2", re.compile(r"\bN\s*2\b(?!\s*O)", re.I)),
    ("O2", re.compile(r"\bO\s*2\b", re.I)),
]

# Longer / more specific patterns first so ranges are not also stored as singles.
PATTERNS: list[tuple[str, str, re.Pattern[str]]] = [
    ("growth_rate", "μm/h", re.compile(r"(\d+(?:\.\d+)?)\s*(?:–|—|-|~|to)\s*(\d+(?:\.\d+)?)\s*(?:μ|µ|u)\s*m\s*/\s*h", re.I)),
    ("growth_rate", "μm/h", re.compile(r"(\d+(?:\.\d+)?)\s*(?:μ|µ|u)\s*m\s*/\s*h", re.I)),
    ("growth_rate", "mm/h", re.compile(r"(\d+(?:\.\d+)?)\s*mm\s*/\s*h", re.I)),
    ("temperature", "°C", re.compile(r"(\d{3,4}(?:\.\d+)?)\s*(?:–|—|-|~|to)\s*(\d{3,4}(?:\.\d+)?)\s*(?:°|º|˚)\s*C")),
    ("temperature", "°C", re.compile(r"(\d{3,4}(?:\.\d+)?)\s*(?:°|º|˚)\s*C")),
    ("energy", "MeV", re.compile(r"(\d+(?:\.\d+)?)\s*(?:–|—|-|to)\s*(\d+(?:\.\d+)?)\s*MeV", re.I)),
    ("energy", "MeV", re.compile(r"(\d+(?:\.\d+)?)\s*MeV", re.I)),
    ("energy", "keV", re.compile(r"(\d+(?:\.\d+)?)\s*(?:–|—|-|to)\s*(\d+(?:\.\d+)?)\s*keV", re.I)),
    ("energy", "keV", re.compile(r"(\d+(?:\.\d+)?)\s*keV", re.I)),
    ("pressure", "kPa", re.compile(r"(\d+(?:\.\d+)?)\s*(?:–|—|-|to)\s*(\d+(?:\.\d+)?)\s*kPa", re.I)),
    ("pressure", "kPa", re.compile(r"(\d+(?:\.\d+)?)\s*kPa", re.I)),
    ("pressure", "Torr", re.compile(r"(\d+(?:\.\d+)?)\s*Torr", re.I)),
    ("dose", "cm-2", re.compile(r"(\d+(?:\.\d+)?)\s*[×x]\s*10\s*\^?\s*(\d+)\s*cm\s*(?:-2|−2|–2)", re.I)),
    ("doping", "cm-3", re.compile(r"(\d+(?:\.\d+)?)\s*[×x]\s*10\s*\^?\s*(\d+)\s*cm\s*(?:-3|−3|–3)", re.I)),
    ("doping", "cm-3", re.compile(r"(?<![\d.])10\s*(\d{1,2})\s*cm\s*(?:-3|−3|–3)", re.I)),
    ("ron", "mΩ·cm²", re.compile(r"(\d+(?:\.\d+)?)\s*m\s*Ω\s*[·.]?\s*cm", re.I)),
    ("breakdown", "kV", re.compile(r"(\d+(?:\.\d+)?)\s*kV\b")),
    ("length", "nm", re.compile(r"(\d+(?:\.\d+)?)\s*nm\b", re.I)),
    ("length", "μm", re.compile(r"(\d+(?:\.\d+)?)\s*(?:–|—|-|to)\s*(\d+(?:\.\d+)?)\s*(?:μ|µ|u)\s*m\b", re.I)),
    ("length", "μm", re.compile(r"(\d+(?:\.\d+)?)\s*(?:μ|µ|u)\s*m\b", re.I)),
    ("wafer", "mm", re.compile(r"\b(100|150|200|300)\s*mm\b")),
    ("wafer", "inch", re.compile(r"\b(\d+(?:\.\d+)?)\s*(?:-|–)?\s*inch", re.I)),
    ("fraction", "%", re.compile(r"(\d+(?:\.\d+)?)\s*(?:–|—|-|to)\s*(\d+(?:\.\d+)?)\s*%")),
    ("fraction", "%", re.compile(r"(\d+(?:\.\d+)?)\s*%")),
]


def clean_page(text: str) -> str:
    text = text.replace("\u00ad", "")
    text = re.sub(r"Return to Technical Program", " ", text)
    text = re.sub(r"©\s*ICSCRM\s*2026[^\n]*", " ", text, flags=re.I)
    text = re.sub(rf"{ID}\s+ICSCRM\s*2026", " ", text, flags=re.I)
    text = re.sub(r"[ \t]+", " ", text)
    return text


def flatten(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def context_at(flat: str, start: int, end: int, n: int = 110) -> str:
    a = max(0, start - n)
    b = min(len(flat), end + n)
    snippet = flat[a:b].strip()
    return re.sub(r"\s+", " ", snippet)


def plausible(kind: str, value: float, value_hi: float | None, unit: str) -> bool:
    hi = value_hi if value_hi is not None else value
    if kind == "temperature":
        return 250 <= value <= 2800 and hi <= 2800 and value not in range(2015, 2031)
    if kind == "energy" and unit == "MeV":
        return 0.05 <= value <= 30
    if kind == "energy" and unit == "keV":
        return 1 <= value <= 20000
    if kind == "pressure":
        return 0 < value <= 1000
    if kind == "growth_rate":
        return 0 < value <= 500
    if kind == "dose":
        return 1e10 <= value <= 1e18
    if kind == "doping":
        return 1e12 <= value <= 1e22
    if kind == "ron":
        return 0.01 <= value <= 500
    if kind == "breakdown":
        return 0.2 <= value <= 30
    if kind == "length" and unit == "nm":
        return 0.2 <= value <= 5000
    if kind == "length" and unit == "μm":
        return 0.01 <= value <= 500
    if kind == "wafer" and unit == "mm":
        return value in {100, 150, 200, 300}
    if kind == "wafer" and unit == "inch":
        return 2 <= value <= 18
    if kind == "fraction":
        return 0 < value <= 100
    return False


def mine(flat: str) -> list[dict]:
    occupied: list[tuple[int, int]] = []
    found: list[dict] = []

    def overlaps(a: int, b: int) -> bool:
        return any(not (b <= c or a >= d) for c, d in occupied)

    for kind, unit, pat in PATTERNS:
        for match in pat.finditer(flat):
            if overlaps(*match.span()):
                continue
            groups = [g for g in match.groups() if g is not None]
            value_hi = None
            if kind in {"dose", "doping"} and unit.startswith("cm") and len(groups) == 2 and "×" in match.group(0) or (
                kind in {"dose", "doping"} and len(groups) == 2 and re.search(r"[×x]|10\s*\^", match.group(0))
            ):
                value = float(groups[0]) * 10 ** int(groups[1])
            elif kind == "doping" and len(groups) == 1 and match.group(0).strip().startswith("10"):
                value = 10 ** int(groups[0])
            elif len(groups) == 2 and kind not in {"dose", "doping"}:
                value = float(groups[0])
                value_hi = float(groups[1])
            else:
                value = float(groups[0])
            if not plausible(kind, value, value_hi, unit):
                continue
            # Percents only count when the sentence is about a process or device metric.
            if kind == "fraction":
                window = flat[max(0, match.start() - 80) : match.end() + 40].lower()
                if not any(w in window for w in ("uniform", "activ", "yield", "rough", "ratio", "mobil", "degrad", "reduc", "improv", "variat")):
                    continue
            occupied.append(match.span())
            found.append({
                "kind": kind,
                "value": value,
                "value_hi": value_hi,
                "unit": unit,
                "context": context_at(flat, match.start(), match.end()),
            })
    return found


def process_sentences(flat: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", flat)
    key = re.compile(
        r"°\s*C|℃|keV|MeV|implant|anneal|epitax|trench|oxid|nitrid|channeling|HCl|SiH|μm/h|µm/h|kPa",
        re.I,
    )
    kept = []
    for sent in parts:
        sent = sent.strip()
        if 50 <= len(sent) <= 420 and key.search(sent):
            kept.append(sent)
        if len(kept) == 6:
            break
    return kept


def gases_in(flat: str) -> list[str]:
    return [name for name, pat in GAS_RULES if pat.search(flat)]


def modules_in(flat: str) -> list[str]:
    return [name for name, pat in MODULE_RULES if pat.search(flat)]


def main() -> None:
    from pypdf import PdfReader

    if not PDF.exists():
        raise SystemExit(f"Missing {PDF}")
    reader = PdfReader(str(PDF))
    buckets: dict[str, list[str]] = defaultdict(list)
    pages: dict[str, list[int]] = defaultdict(list)
    current = None
    # Plenary abstracts start around page 11; the oral/poster bodies start at page 56.
    for i in range(9, len(reader.pages)):
        raw = reader.pages[i].extract_text() or ""
        head = HEADER.search(raw[:400])
        if head:
            current = head.group(1)
        if current:
            buckets[current].append(clean_page(raw))
            pages[current].append(i + 1)
        if (i + 1) % 200 == 0:
            print(f"page {i+1}", flush=True)

    DATA.mkdir(parents=True, exist_ok=True)
    abs_path = DATA / "abstracts.jsonl"
    fact_path = DATA / "paper_facts.jsonl"
    sig_path = DATA / "signals.jsonl"
    n_sig = 0
    with abs_path.open("w", encoding="utf-8") as fa, fact_path.open("w", encoding="utf-8") as ff, sig_path.open("w", encoding="utf-8") as fs:
        for pid in sorted(buckets):
            text = "\n".join(buckets[pid])
            text = HEADER.sub(" ", text)
            text = re.sub(r"\(continued\)", " ", text, flags=re.I)
            flat = flatten(text)
            signals = mine(flat)
            temps = [s["value"] for s in signals if s["kind"] == "temperature"]
            mods = modules_in(flat)
            fact = {
                "id": pid,
                "pdf_page": pages[pid][0],
                "pdf_pages": pages[pid],
                "n_chars": len(flat),
                "gases": gases_in(flat),
                "text_modules": mods,
                "temp_min": min(temps) if temps else None,
                "temp_max": max(temps) if temps else None,
                "n_signals": len(signals),
                "process_sentences": process_sentences(flat),
            }
            ff.write(json.dumps(fact, ensure_ascii=False) + "\n")
            fa.write(json.dumps({"id": pid, "pdf_page": pages[pid][0], "text": flat}, ensure_ascii=False) + "\n")
            for sig in signals:
                sig["id"] = pid
                sig["pdf_page"] = pages[pid][0]
                fs.write(json.dumps(sig, ensure_ascii=False) + "\n")
                n_sig += 1
    print(f"abstracts {len(buckets)} signals {n_sig}")


if __name__ == "__main__":
    main()
