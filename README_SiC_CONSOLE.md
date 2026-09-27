# SiC Learning & R&D Console

Streamlit knowledge console converting the **ICSCRM 2026 Tutorial** into an expandable SiC engineering knowledge system.

## Scope
Material → crystal/epitaxy → defects → process → MOS interface → devices → reliability → modules → systems.

Deep dives: trench/FinFET, SiC superjunction, bipolar degradation, BTI/GSI/REDR, module integration, Infineon architecture map and SiC JFET.

## Evidence discipline
- **Tutorial direct** — explicitly supported by tutorial
- **Tutorial-derived** — synthesis from tutorial material
- **Engineering model** — simplified calculator/model
- **Frontier** — verify against primary literature

The source PDF is intentionally not committed; local PDFs under `sources/` are ignored.

## Run
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
