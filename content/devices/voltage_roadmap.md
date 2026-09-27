# SiC Architecture Roadmap — Evidence-Aware Matrix

This is a **technology-selection hypothesis**, not an industry-standard boundary map.

| Voltage region | Candidate architecture | Process direction | Evidence status |
|---|---|---|---|
| ~1.2 kV | Trench MOSFET / Semi-SJ exploration | Channeling implant, multi-epi, TFE are candidates | 🟢 Harada demonstrates 1.2 kV SJ routes; 🟠 commercial choice is application/cost dependent |
| 1.2–3.3 kV | Short-/Semi-/Full-SJ MOSFET | Channeling ↔ TFE transition study | 🟢 Harada shows 1.2 & 3.3 kV data; 🟠 “golden zone” is a strategy hypothesis |
| 3.3–6.5 kV | Full-SJ / high-voltage MOSFET research | deeper TFE increasingly attractive | 🟢 tutorial says TFE becomes more attractive as columns deepen; 🟣 exact 6.5 kV boundary requires evidence |
| ~10 kV+ | SiC IGBT becomes an important candidate | thick epi + low-resistivity p-type collector are critical | 🟢 Harada tutorial explicitly highlights IGBT potential for 10 kV class and above |

## Do not hard-code as facts yet
- “Rdrift = 30–40% at ≤1.2 kV” or “60–80% at 1.2–3.3 kV”
- “TFE requires >20 µm pillars” as a universal crossover
- “SJ exits competition above 10 kV”
- “IGBT requires 60–90 µm pillar depth” (pillar terminology is not appropriate for an IGBT drift design)

These should become device-/paper-specific cards after source verification.
