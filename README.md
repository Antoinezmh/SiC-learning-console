# ⚡ SiC Learning & R&D Console

> **From tutorial notes to an engineering knowledge system for SiC power devices.**

A Streamlit-based learning and R&D console that starts from the **ICSCRM 2026 Tutorial** and grows into a structured knowledge base for **SiC material, epitaxy, defects, MOS interface, trench MOSFET, superjunction, reliability, packaging/modules and system applications**.

The goal is not to make another collection of slides. It is to connect:

**Physics → Material / Process → Device Structure → Electrical Behavior → Reliability → Productization → System Value**

---

## 🎯 Why this project

SiC knowledge is usually fragmented across textbooks, conference tutorials, papers, datasheets, TCAD work and internal engineering experience. This project organizes those layers into one reusable engineering framework.

It is designed for three modes:

1. **Learn** — understand the physical mechanism and terminology.
2. **Analyze** — connect structure/process changes to device behavior.
3. **Engineer** — turn knowledge into design questions, calculators, comparison frameworks and R&D decisions.

---

## 🧭 Knowledge architecture

```text
Material Physics
      ↓
Crystal / Epitaxy
      ↓
Defects & Lifetime
      ↓
Process Technology
      ↓
MOS Interface
      ↓
Device Architecture
      ↓
Reliability & Ruggedness
      ↓
Packaging / Module
      ↓
Power Electronics System
```

Cross-layer reasoning is emphasized. For example:

```text
BPD
 ↓
carrier recombination
 ↓
stacking-fault expansion
 ↓
minority-carrier lifetime / on-state degradation
 ↓
body-diode strategy & qualification
```

---

## 📚 Current source pack

### ICSCRM 2026 Tutorial

The first knowledge pack follows five tutorial themes:

| Tutorial theme | Knowledge extracted into the console |
|---|---|
| Fundamentals of SiC Power Semiconductors | material/device physics, bulk growth, epitaxy, lifetime, extended defects, MOS transport |
| SiC in Modern Power Electronics | efficiency, power density and system architecture |
| Next Generation SiC Power Devices | superjunction, high-voltage devices and emerging architectures |
| Material Perturbation → Device Degradation | defect kinetics, oxide traps, BTI/GSI and degradation modeling |
| SiC Power Modules | thermal design, bonding, low-inductance integration and gate drive |

The original tutorial PDF is intentionally **not committed** to this repository.

---

## 🏗️ Current modules

```text
SiC-learning-console/
├── app.py
├── README_SiC_CONSOLE.md
├── requirements.txt
├── .gitignore
└── pages/
    ├── 01_Knowledge_Map.py
    ├── 02_ICSCRM_2026_Pack.py
    ├── 03_MOS_Trench_FinFET.py
    ├── 04_Superjunction.py
    ├── 05_Defects_Bipolar.py
    ├── 06_Reliability_REDR.py
    ├── 07_Module_WPT.py
    ├── 08_Infineon_Devices.py
    ├── 09_SiC_JFET_Deep_Dive.py
    └── 10_Engineering_Tools.py
```

### Module focus

| Module | Main questions |
|---|---|
| Knowledge Map | How do material → device → system knowledge layers connect? |
| ICSCRM 2026 Pack | What are the tutorial's major technical anchors? |
| MOS / Trench / FinFET | How do interface charge, mobility, trench geometry and oxide field interact? |
| **SiC Superjunction** | How do charge balance, P/N columns, process route and temperature determine SJ performance? |
| Defects / Bipolar | How do BPD, stacking faults, carbon vacancies and lifetime affect devices? |
| Reliability / REDR | How should BTI, GSI and defect reactions be interpreted and verified? |
| Module / Low-L | How do thermal, parasitic and gate-drive design unlock SiC performance? |
| Infineon Devices | How can commercial device evolution be analyzed by architecture rather than catalog? |
| SiC JFET | Why does a bulk-channel JFET differ fundamentally from a MOSFET? |
| Engineering Tools | How can first-order models turn learning into quantitative intuition? |

---

# ⭐ SiC Superjunction Deep Dive

Superjunction is one of the main deep-dive tracks in this repository.

## 1. Core physical idea

Alternating P/N regions provide **charge compensation**, reshaping the drift-region electric field.

A useful first-order representation is:

```text
QN = q · ND · WN
QP = q · NA⁻ · WP

Ideal charge balance:
QN ≈ QP
```

For SiC, the effective ionized acceptor concentration `NA⁻` is important because **p-type incomplete ionization** can make the electrically active charge different from the nominal Al concentration.

This immediately creates an engineering question:

> Does a charge balance optimized at room temperature remain optimal at 175–200 °C?

## 2. Process routes

The tutorial motivates two important routes:

### High-energy channeling implantation
Potential advantages / questions:
- process-cycle-time attractiveness
- achievable P-column depth
- implantation damage
- activation
- lateral and vertical dose control

### Trench filling / epitaxial filling
Potential advantages / questions:
- increasing attractiveness for deeper columns
- deep-trench profile control
- epitaxial fill quality
- defects / interfaces
- wafer-scale uniformity

The important product question is therefore not only:

> **Can a SiC SJ device be demonstrated?**

but:

> **Can charge balance be controlled across wafer, lot, temperature, lifetime and manufacturing variation?**

## 3. SJ evaluation matrix

```text
Physics
  ↓
Charge Balance
  ↓
P/N Column Structure
  ↓
Process Route
  ↓
Static Performance
BV / Ron,sp / Ron(T)
  ↓
Dynamic Performance
Qrr / Coss / Crss / switching
  ↓
Ruggedness
SC / avalanche / forward current
  ↓
Manufacturability
process window / uniformity / yield / cost
```

The console therefore deliberately avoids reducing SJ to only **“lower Ron”**.

---

## 🔬 MOS / Trench / FinFET track

A first-order resistance decomposition is used throughout the console:

```text
Ron =
Rch
+ Racc
+ RJFET
+ Rdrift
+ Rsub
+ Rcontact
```

This encourages generation-to-generation device analysis to ask **which resistance component actually improved**.

The MOS-interface track also separates:

- free carriers
- trapped charge
- free-carrier mobility
- apparent channel mobility

so that interface engineering is not interpreted only through a single measured mobility value.

---

## 🧬 Defects & bipolar degradation

Key learning chain:

```text
BPD
 + carrier recombination
        ↓
stacking-fault expansion
        ↓
carrier lifetime / electrical degradation
        ↓
device & body-diode reliability
```

The console also connects **Z1/2 / carbon vacancy**, carrier lifetime engineering and recombination-enhancing layers to device design.

---

## 🛡️ Reliability framework

Reliability is organized around causal evidence rather than a single electrical symptom:

```text
Stress
  ↓
Material change
  ↓
Defect location
  ↓
Electrical signature
  ↓
Physical model
  ↓
Independent verification
```

Current topics include:

- BTI
- GSI
- interface / border / near-interface traps
- SRH capture and emission
- tunneling-assisted trapping
- REDR-related modeling

> One electrical symptom can have multiple physical origins. Mechanism identification should rely on converging evidence.

---

## ⚡ SiC JFET Deep Dive

The JFET track is included to compare two fundamentally different approaches to SiC conduction.

### MOSFET

```text
Source
 ↓
SiC/SiO₂ inversion channel
 ↓
accumulation / JFET region
 ↓
drift region
 ↓
Drain
```

### JFET

```text
Source
 ↓
bulk SiC channel
 ↓
drift region
 ↓
Drain
```

A SiC JFET therefore avoids the inversion-channel interface penalty, but a conventional power JFET is **normally-on**, moving part of the engineering challenge from device physics into gate drive, fail-safe architecture and system protection.

Current JFET topics:

- depletion / pinch-off physics
- normally-on operation
- bulk-channel resistance
- dual-drive concepts
- cascode concepts
- solid-state circuit breaker / protection applications

---

## 🏭 Commercial-device learning track

The Infineon page is intentionally structured as a **technology map rather than a product catalog**.

Current architecture families include:

- SiC Schottky barrier diode
- CoolSiC MOSFET generation evolution
- SiC JFET
- cascode concepts
- hybrid Si/SiC switch concepts
- SiC power modules

The analysis template asks:

```text
What physical bottleneck changed?
        ↓
What structure/process changed?
        ↓
Which part of Ron changed?
        ↓
What happened to Qgd / Crss?
        ↓
What happened to oxide/body-diode stress?
        ↓
What happened to SC / avalanche?
        ↓
What manufacturing complexity was added?
```

Current commercial-device information should always be checked against official manufacturer documentation before being treated as a product specification.

---

## 🧮 Engineering tools

The current Streamlit version contains first-order interactive tools for:

### SiC unipolar-limit exploration

```text
Ron,sp = 2.8 × 10⁻¹¹ × VB^2.28   Ω·cm²
```

### MOSFET resistance budget

Interactive decomposition of:

```text
Rch + Racc + RJFET + Rdrift + Rsub + Rcontact
```

### Module common-mode current

```text
Icm = Cpar × dv/dt
```

These are **learning / engineering models**, not sign-off simulation models.

---

## 🏷️ Evidence discipline

Every knowledge item should ultimately carry an evidence label:

| Label | Meaning |
|---|---|
| 🟢 Tutorial direct | Explicitly supported by the source tutorial |
| 🔵 Tutorial-derived | Engineering synthesis based on tutorial content |
| 🟠 Engineering model | Simplified quantitative/physical model |
| 🟣 Frontier / verify | Interesting research direction requiring primary-source verification |

This distinction is intentional: **source fact, engineering interpretation and research hypothesis should not silently become mixed together.**

---

## 🚀 Run locally

### 1. Clone

```bash
git clone https://github.com/Antoinezmh/SiC-learning-console.git
cd SiC-learning-console
```

### 2. Create environment

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 3. Install

```bash
pip install -r requirements.txt
```

### 4. Run

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

---

## 🛣️ Roadmap

### V1 — Knowledge skeleton
- [x] Streamlit multipage console
- [x] ICSCRM 2026 tutorial pack
- [x] MOS / trench knowledge page
- [x] Superjunction deep dive
- [x] defects & bipolar degradation
- [x] reliability framework
- [x] module / low-inductance page
- [x] Infineon architecture map
- [x] SiC JFET deep dive
- [x] first engineering calculators

### V2 — Structured knowledge base
- [ ] YAML/JSON knowledge cards
- [ ] source/page-level references
- [ ] searchable knowledge nodes
- [ ] equation library
- [ ] defect/process/device database
- [ ] research notebook

### V3 — Device engineering
- [ ] temperature-dependent Ron model
- [ ] incomplete-ionization calculator
- [ ] SJ charge-balance/process-window model
- [ ] trench electric-field design cards
- [ ] switching-loss calculator
- [ ] reliability test matrix
- [ ] competitor/device comparison database

### V4 — AI for Power
- [ ] RAG over tutorials/papers/internal notes
- [ ] natural-language engineering search
- [ ] knowledge graph
- [ ] automatic paper ingestion
- [ ] source-aware technical Q&A
- [ ] TCAD / experiment / reliability workflow integration

---

## 🔭 Long-term vision

The long-term target is an **AI-for-Power engineering workspace**, not just a learning website:

```text
Tutorials + Papers + Datasheets + Experiments + TCAD + Internal Knowledge
                              ↓
                     SiC Knowledge Core
                              ↓
            AI-assisted engineering reasoning
                              ↓
Requirement → Design → Epi → Process → Validation
          → Reliability → Application → Production
```

The repository is currently an early engineering knowledge prototype and will continue to evolve as additional conference material, papers and verified device data are incorporated.
