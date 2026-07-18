# Data Enrichment Log

## Added 2026-07-18 by Betel Yohannes

### Observations (5)
- REC_0034–0036: Account ownership disaggregated by urban location, male, and female (2024 Findex round) — fills gap noted in Task 1 instructions on gender/regional disaggregation.
- REC_0037: Recomputed 2024 gender gap (15pp, high confidence) from REC_0035/0036, superseding the prior estimated 18pp figure (REC_0028). Both retained; discrepancy flagged for EDA discussion.
- REC_0038: New indicator `USG_DIGITAL_ENABLED` (7%, 2024) — captures the access-vs-usage gap central to the challenge brief.

Source: Global Findex 2024, via Shega/DFS Ethiopia Hub and Birr Metrics reporting.

### Events (1)
- EVT_0011: Banking Business Proclamation No. 1360/2024 (Dec 17, 2024) — Ethiopia's first opening of its banking sector to foreign banks in ~50 years. Not previously captured; relevant infrastructure/regulatory context for Access forecasting.

### Impact Links (2)
- IMP_0015: EVT_0011 → ACC_OWNERSHIP (enabling, low, 36mo lag, theoretical) — too recent for empirical Ethiopian evidence.
- IMP_0016: EVT_0009 (NFIS-II) → ACC_OWNERSHIP (enabling, medium, 24mo lag, theoretical) — previously had zero modeled impact despite being the flagship policy with the 70% target.

### Rationale
All additions directly address gaps identified during initial exploration: (1) no urban/rural or gender-disaggregated data beyond 2021, (2) NFIS-II had no modeled effect on its own target indicator, (3) no infrastructure/regulatory events post-2024 captured.
