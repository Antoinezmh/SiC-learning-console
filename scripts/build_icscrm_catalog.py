"""Build the ICSCRM 2026 catalog from the local abstract-book program pages.

Reads References/ICSCRM2026_AbstractBook23_092526.pdf pages 22–55
(technical program + detailed poster program) and writes data/catalog.jsonl.
Process cards are maintained separately in data/process_cards.jsonl.
"""

from __future__ import annotations

import json
import re
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "References" / "ICSCRM2026_AbstractBook23_092526.pdf"
OUT = ROOT / "data" / "catalog.jsonl"

ID_CORE = (
    r"(?:(?:Mo|Tu|We|Th|Fr)-(?:P|PL|IP|[123][AB])-\d{2}(?:LN)?|IP-\d{2})"
)
DAY_RE = re.compile(
    r"^(Monday|Tuesday|Wednesday|Thursday|Friday),\s+\w+\s+\d+"
)
TRACK_RE = re.compile(r"^Track\s+(\d+)\s+(.+)$")
SESSION_RE = re.compile(
    r"^((?:Mo|Tu|We|Th|Fr)-\d[AB]):\s*(.+)$"
)
AFF_RE = re.compile(r"^\d+\s*\.")
PAGE_NUM_RE = re.compile(r"^\d{1,4}$")
AUTHOR_START = re.compile(
    r"\s((?:[A-Z][\w'’.\-]+)(?:\s+[A-Z][\w'’.\-]+){0,5}\d)\b"
)
SESSION_CODE = re.compile(r"^((?:Mo|Tu|We|Th|Fr)-\d[AB])")
PREFIX_DAY = {
    "Mo": "Monday",
    "Tu": "Tuesday",
    "We": "Wednesday",
    "Th": "Thursday",
    "Fr": "Friday",
    "IP": "",
}

MODULE_RULES: list[tuple[str, re.Pattern[str]]] = [
    ("sj", re.compile(r"super[\s-]?junction|\bpillars?\b|charge balance", re.I)),
    ("trench", re.compile(r"trench|corner round|etch damage|dry etch", re.I)),
    ("implant", re.compile(r"implant|channeling|dopant activation|activation anneal", re.I)),
    ("gate_stack", re.compile(
        r"\bMOS\b|SiO2|oxide|nitrid|\bNO anneal\b|MOS interface|channel mobility|gate stack|gate dielectric",
        re.I,
    )),
    ("epi", re.compile(r"epitax|epilayer|homoepitax|thin[- ]film|C/Si|CVD growth", re.I)),
    ("bulk", re.compile(
        r"bulk|PVT|HTCVD|sublimation|boule|solution growth|TSSG|wafer|crystal growth",
        re.I,
    )),
    ("contact", re.compile(r"contact|schottky|ohmic|metalliz", re.I)),
    ("defect", re.compile(
        r"dislocation|stacking fault|\bBPD\b|micropipe|lifetime|vacanc|point defect",
        re.I,
    )),
    ("reliability", re.compile(
        r"reliab|\bBTI\b|short-circuit|rugged|degrad|bias temperature|single-event",
        re.I,
    )),
    ("quantum", re.compile(r"quantum|qubit|color center|silicon vacanc", re.I)),
    ("device", re.compile(r"MOSFET|IGBT|\bJBS\b|JFET|FinFET|diode|\bSBD\b|HEMT", re.I)),
]
PROCESS_MODULES = {"sj", "trench", "implant", "gate_stack", "epi", "bulk", "contact"}


def kind_of(pid: str) -> str:
    if "-PL-" in pid:
        return "plenary"
    if pid.startswith("IP-") or "-IP" in pid:
        return "invited_poster"
    if "-P-" in pid:
        return "poster"
    return "oral"


def parse_id(line: str) -> tuple[str, str] | None:
    s = line.strip()
    s = re.sub(r"^\d{2}:\d{2}\s+", "", s)
    invited = "Invited" if re.search(r"\(Invited\)", s) else ""
    s = re.sub(r"\s*\(Invited\)\s*$", "", s).strip()
    if re.fullmatch(ID_CORE, s):
        return s, invited
    return None


def join_wrapped(lines: list[str]) -> str:
    out = ""
    for line in lines:
        piece = re.sub(r"\s+", " ", line).strip()
        if not piece:
            continue
        if not out:
            out = piece
        elif out.endswith("-"):
            out += piece
        else:
            out += " " + piece
    return re.sub(r"\s+", " ", out).strip()


def peel_authors(title: str) -> tuple[str, str]:
    """Split a title when the PDF joined the first author onto the same line."""
    match = AUTHOR_START.search(title)
    if not match or match.start() < 40:
        return title, ""
    return title[: match.start()].strip(" -"), title[match.start() :].strip()


def split_head(lines: list[str]) -> tuple[str, str, str]:
    """Return title, authors, orgs from the lines of one program entry."""
    cleaned = [re.sub(r"\s+", " ", ln).strip() for ln in lines]
    cleaned = [ln for ln in cleaned if ln and not PAGE_NUM_RE.fullmatch(ln)]
    if not cleaned:
        return "", "", ""
    aff_idx = next((i for i, ln in enumerate(cleaned) if AFF_RE.match(ln)), None)
    if aff_idx is None:
        head, org_lines = cleaned, []
    else:
        head, org_lines = cleaned[:aff_idx], cleaned[aff_idx:]
    presenter = next((i for i, ln in enumerate(head) if "○" in ln), None)
    if presenter is None:
        title = join_wrapped(head)
        authors = ""
    else:
        title = join_wrapped(head[:presenter])
        authors = join_wrapped(head[presenter:])
    extra_title, extra_authors = peel_authors(title)
    if extra_authors:
        title = extra_title
        authors = f"{extra_authors} {authors}".strip()
    orgs = join_wrapped(org_lines)
    authors = authors.replace("○", "").strip(" ,")
    if title.lower() == "withdrawn":
        return "Withdrawn", "", ""
    return title, authors, orgs


def modules_for(title: str) -> list[str]:
    return [name for name, pat in MODULE_RULES if pat.search(title)]


def page_lines(reader, start: int, end: int) -> list[tuple[int, str]]:
    rows: list[tuple[int, str]] = []
    for i in range(start, end):
        text = reader.pages[i].extract_text() or ""
        for raw in text.splitlines():
            line = raw.strip()
            if not line or PAGE_NUM_RE.fullmatch(line):
                continue
            if line.startswith("====="):
                continue
            rows.append((i + 1, line))
    return rows


def parse_program(rows: list[tuple[int, str]]) -> list[dict]:
    day = ""
    track = ""
    track_buf: list[str] = []
    session_names: dict[str, str] = {}
    records: list[dict] = []
    current: dict | None = None
    buf: list[str] = []

    def flush() -> None:
        nonlocal current, buf
        if current is None:
            buf = []
            return
        title, authors, orgs = split_head(buf)
        current["title"] = title
        current["authors"] = authors.replace("○", "").strip(" ,")
        current["orgs"] = orgs
        current["status"] = "withdrawn" if title == "Withdrawn" else "active"
        mods = modules_for(title)
        current["modules"] = mods
        current["primary_module"] = next(
            (m for m in mods if m in PROCESS_MODULES), mods[0] if mods else "other"
        )
        current["process_relevant"] = current["primary_module"] in PROCESS_MODULES
        code = SESSION_CODE.match(current["id"])
        if current["kind"] == "oral" and code:
            label = current.get("_session_names", {}).get(code.group(1), "")
            current["session"] = f"{code.group(1)} {label}".strip()
        current.pop("_session_names", None)
        records.append(current)
        current = None
        buf = []

    def close_track() -> None:
        nonlocal track, track_buf
        if track_buf:
            track = join_wrapped(track_buf)
            track = re.split(r"\s+\(", track, maxsplit=1)[0].strip()
            track_buf = []

    for page, line in rows:
        if line in {
            "Detailed Poster Program",
            "Lunch",
            "Announcement",
            "Opening (9:00-9:10, 1st Floor)",
        }:
            continue
        if line.startswith("Detailed poster program"):
            continue
        if line.startswith("Session Chair:") or line.startswith("Oral-A") or line.startswith("Oral-B"):
            continue
        if line.startswith("Oral Sessions") or line.startswith("Poster Session") or line.startswith("Plenary"):
            continue
        if line.startswith("Invited Poster") or line.startswith("Banquet") or line.startswith("Registration"):
            continue
        day_m = DAY_RE.match(line)
        if day_m:
            flush()
            close_track()
            day = day_m.group(1)
            track = ""
            continue
        if line.startswith("Track "):
            flush()
            close_track()
            track_buf = [line]
            continue
        if track_buf and parse_id(line) is None and not SESSION_RE.match(line):
            # wrapped track header
            if not AFF_RE.match(line):
                track_buf.append(line)
                continue
        close_track()
        sess = SESSION_RE.match(line)
        if sess and parse_id(line) is None:
            flush()
            session_names[sess.group(1)] = re.sub(r"\s+", " ", sess.group(2)).strip()
            continue
        parsed = parse_id(line)
        if parsed:
            flush()
            pid, invited = parsed
            prefix = pid.split("-")[0]
            current = {
                "id": pid,
                "kind": kind_of(pid),
                "invited": bool(invited),
                "day": day or PREFIX_DAY.get(prefix, ""),
                "track": track if "-P-" in pid else "",
                "session": "",
                "program_page": page,
                "_session_names": session_names,
                "source": "ICSCRM 2026 Abstract Book, program pages",
            }
            buf = []
            continue
        if current is not None:
            buf.append(line)
    flush()
    return records


def main() -> None:
    from pypdf import PdfReader

    if not PDF.exists():
        raise SystemExit(f"Missing abstract book: {PDF}")
    reader = PdfReader(str(PDF))
    # Program at a glance is image-heavy; the parsable program is pp. 22–55.
    rows = page_lines(reader, 21, 55)
    records = parse_program(rows)
    # Drop empty shells created by session furniture that looked like IDs.
    records = [r for r in records if r.get("title") or r.get("status") == "withdrawn"]
    # Stable order: day, kind, id
    day_order = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "": 9}
    kind_order = {"plenary": 0, "invited_poster": 1, "oral": 2, "poster": 3}
    records.sort(key=lambda r: (day_order.get(r["day"], 9), kind_order.get(r["kind"], 9), r["id"]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    n_proc = sum(1 for r in records if r["process_relevant"] and r["status"] == "active")
    print(f"wrote {len(records)} records ({n_proc} process-relevant) -> {OUT}")


if __name__ == "__main__":
    main()
