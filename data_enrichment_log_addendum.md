# Data Enrichment Log — Addendum (Task 3/4 prep)

## Added 2026-07-19 by Betel Yohannes

### Critical gap fix: Usage pillar target indicator was missing

While preparing Task 3/4, discovered the dataset had **no observation for
`USG_DIGITAL_PAYMENT`** (Digital Payment Adoption Rate) — the actual Usage
metric this entire project is meant to forecast, as defined in the
assignment brief itself. Added two sourced observations to close this gap:

- **REC_0039**: 20% (2021) — World Bank blog citing Global Findex 2021
  ("Only 42 percent of account holders — 20 percent of adults — used their
  accounts for digital payments"). High confidence.
- **REC_0040**: 35% (2024) — figure given directly in the assignment brief's
  Overview section. Medium confidence, since an independent source (Shega/DFS
  Ethiopia Hub) describes 2024 digital payment usage as "fewer than one in
  four adults" (~24%), which conflicts with the brief's ~35%. The brief's
  figure was used since it is the explicit forecasting target for this
  project; the discrepancy is flagged here as a data quality caveat rather
  than silently resolved.

This brings the working dataset to 67 records (35 + 2 = 37 observations, plus
16 impact_links, 11 events, 3 targets).
