# SiC Superjunction — Verified Engineering Knowledge Cards

> Evidence rule: 🟢 = explicitly supported by the ICSCRM 2026 Harada tutorial.  
> 🟠 = engineering interpretation/model. 🟣 = pending independent/primary-source verification.

## 1. Manufacturing process cycle time 🟢

Harada slides 15–16 define **process cycle time** as total processing time from wafer loading to unloading. It is **not a cost figure** and excludes equipment depreciation.

| Route | 1.2 kV / 5 µm column | 3.3 kV / 10 µm column |
|---|---:|---:|
| non-SJ UMOS baseline | 1.00 | 1.00 |
| Multi-epi | 0.75 (8 layers) | 1.50 (16 layers) |
| Trench filling | 0.23 | 0.29 |
| MeV implantation | 0.20 (5 MeV / 2 layers) | 0.45 (5 MeV / 4 layers) |
| Channeling implantation | **0.08 (5 MeV)** | **0.21 (5 MeV / 2 layers)** |

**Tutorial conclusion:** channeling implantation offers the shortest process flow; trench filling becomes more advantageous as voltage class / column depth increases.

### Trench filling 🟢
- Adding HCl suppresses void formation by minimizing mesa over-growth.
- Tilted growth is suppressed by accurate alignment to the [11-20] direction.
- Precise orientation-flat control is required.
- Ref: R. Kosugi et al., JJAP 56, 04CR05 (2017); tutorial also cites S. Ji et al. for trench-filling development.

### Channeling implantation 🟢
- 5 MeV Al channeling along <0001> gives a much deeper range than random implantation at the same energy.
- Precise crystal-axis alignment is required.
- Refs: M. Belanche et al., MSSP 179, 108461 (2024); F. Mazzamuto et al., ICSCRM 2025.

## 2. Bipolar degradation / double implantation 🟢

At the tutorial's high-forward-current degradation comparison:

| Device | ΔVf |
|---|---:|
| UMOS | 21.2% |
| SI-SJUMOS | 5.9% |
| DI-SJUMOS (Al + P) | **0.48% max** |

Harada states that Al + P double implantation introduces many point defects and that ion mass, as well as dose, has a large effect.

Ref: K. Takenaka et al., JJAP 64, 02SP43 (2025).

**Engineering interpretation 🟠:** point defects can act as recombination/lifetime-control centers and thereby suppress carrier-assisted stacking-fault expansion. The exact microscopic defect species should not be asserted without the primary defect-characterization evidence.

## 3. Dynamic incomplete ionization 🟢

- Delayed ionization causes temporary p-column charge imbalance during turn-off.
- Highly doped n-columns suffer degraded ionization ratio and mobility.
- The tutorial presents a lightly doped, wide n-column asymmetric structure as preferable.
- Delayed ionization is linked to soft reverse recovery of the body diode.

Refs:
- D. Nazareno et al., IEEE TED 65, 4469 (2018)
- D. Iizasa et al., SST 40, 125010 (2025)
- T. Tawara et al., MSSP 176, 108324 (2024)

## 4. Short-circuit ruggedness 🟢

- Semi-SJ: tSC = **15.0 µs**
- UMOS: tSC = **13.0 µs**
- Tutorial statement: SJ tSC is about **15% longer**.
- RonA–ESC trade-off improves with SJ.
- At the tutorial comparison point, ESC advantage is **+13% at RT** and **+53% at 175°C**.
- Deep electric-field peak produces a deeper hot spot; the hot spot is farther from the surface metal.

Ref: M. Okada et al., ISPSD 2020, p.70.

## 5. Avalanche ruggedness 🟢

For the cited 3.3 kV-class SJ-MOSFET:
- avalanche current density: **1000 A/cm²**
- improved JTE: **EAS ≈ 13.4 J/cm²**

Ref: S. Matsunaga et al., ISPSD 2025, p.29.

## 6. Design implications 🟠

The combined tutorial evidence suggests that SJ optimization should be treated as a multi-objective problem:

```
Column geometry / doping
        ↓
static charge balance
        ↓
temperature + ionization
        ↓
transient charge balance
        ↓
Ron(T) / Qrr / switching
        ↓
SC hot-spot location / avalanche
        ↓
process window / cycle time / yield
```

A manufacturable optimum may therefore differ from the nominal QP/QN = 1 electrostatic optimum.
