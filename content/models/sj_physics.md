# SJ Physical Formulation Layer

## Evidence status

This file deliberately separates **established SJ theory**, **idealized engineering equations**, and **heuristics**.

### Established literature 🔷
Classical 2-D SJ theory derives electric-field/BV relationships and shows that charge imbalance can strongly reduce breakdown voltage. Relevant starting points:
- T. Fujihira, *Theory of Semiconductor Superjunction Devices*, JJAP 36, 6254–6262 (1997), DOI 10.1143/JJAP.36.6254.
- E. Napoli et al., *The Effect of Charge Imbalance on Superjunction Power Devices: An Exact Analytical Solution*, IEEE EDL 29, 249–251 (2008), DOI 10.1109/LED.2007.915375.
- H. Wang, E. Napoli, F. Udrea, *Breakdown Voltage for Superjunction Power Devices With Charge Imbalance*, IEEE TED 56, 3175–3183 (2009), DOI 10.1109/TED.2009.2032595.
- A. K. et al., *Optimum Aspect Ratio of Superjunction Pillars Considering Charge Imbalance*, IEEE TED (2021), DOI 10.1109/TED.2021.3060684.

These works support the qualitative engineering conclusion: **charge balance, pillar aspect ratio and breakdown voltage are coupled; practical optimum aspect ratio is finite when imbalance is present.**

### Idealized equations 🟠
For learning and first-order comparison only:

```
1-D triangular field:
VB ≈ Ec WD / 2
Ron,sp ≈ 4 VB² / (ε μn Ec³)

Ideal balanced-SJ scaling:
VB ≈ Ec,vertical Lcolumn
ND,max ≈ ε Ec,lateral / (q Wn)
Ron,sp,SJ ≈ 2 VB Wn / (ε μn Ec,lateral)
```

These equations illustrate why an ideal balanced SJ can approach a much weaker BV dependence than a conventional 1-D drift region. They are **not** a substitute for anisotropic 2-D avalanche integration or TCAD.

### Charge-imbalance heuristic 🟠
The UI may optionally visualize

```
Vactual / Videal = 1 / (1 + k |δ| AR)
```

as a tunable sensitivity heuristic. It must **not** be presented as the classical exact analytical solution. For quantitative work use a literature-derived 2-D model or TCAD.

## Incomplete ionization

Harada tutorial directly supports **dynamic incomplete ionization** and delayed p-column charge establishment during turn-off. 🟢

A generic acceptor occupancy/emission formulation can be used as a modeling scaffold, but fixed values such as `EA = 190 meV`, degeneracy `gA = 4`, or a claimed room-temperature microsecond time constant are **material/model dependent and are not promoted to Tutorial-direct constants here**. They require calibration against the selected Al concentration, band model and primary source.

Recent external work also analyzes temperature-dependent incomplete ionization in multi-kV 4H-SiC SJ devices (PSS(a), 2026, DOI 10.1002/pssa.202500976). 🔷
