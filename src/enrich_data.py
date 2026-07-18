import pandas as pd
from datetime import date

TODAY = str(date.today())
COLLECTOR = "Betel Yohannes"

path = "data/raw/ethiopia_fi_unified_data.xlsx"
main = pd.read_excel(path, sheet_name="ethiopia_fi_unified_data")
impact = pd.read_excel(path, sheet_name="Impact_sheet")

# ---------- NEW OBSERVATIONS ----------
new_obs = [
    dict(record_id="REC_0034", record_type="observation", pillar="ACCESS",
         indicator="Account Ownership Rate", indicator_code="ACC_OWNERSHIP",
         indicator_direction="higher_better", value_numeric=73, value_type="percentage",
         unit="%", observation_date="2024-11-29", fiscal_year=2024, gender="all",
         location="urban", source_name="Global Findex 2024 (via Shega/DFS Ethiopia Hub)",
         source_type="research", source_url="https://digitalfinance.shega.co/insights/articles/findex-2025-and-ethiopia-s-digital-financial-leap-momentum-without-maturity",
         confidence="high", collected_by=COLLECTOR, collection_date=TODAY,
         original_text="in urban areas, the figure stood at 73%",
         notes="Urban account ownership disaggregation, 2024 Findex round"),

    dict(record_id="REC_0035", record_type="observation", pillar="ACCESS",
         indicator="Account Ownership Rate", indicator_code="ACC_OWNERSHIP",
         indicator_direction="higher_better", value_numeric=57, value_type="percentage",
         unit="%", observation_date="2024-11-29", fiscal_year=2024, gender="male",
         location="national", source_name="Global Findex 2024 (via Birr Metrics)",
         source_type="research", source_url="https://birrmetrics.com/49-of-ethiopians-are-banked-as-findex-2025-highlights-the-next-inclusion-challenge/",
         confidence="high", collected_by=COLLECTOR, collection_date=TODAY,
         original_text="57 percent of men in Ethiopia report having an account",
         notes="Male account ownership, 2024 Findex round"),

    dict(record_id="REC_0036", record_type="observation", pillar="ACCESS",
         indicator="Account Ownership Rate", indicator_code="ACC_OWNERSHIP",
         indicator_direction="higher_better", value_numeric=42, value_type="percentage",
         unit="%", observation_date="2024-11-29", fiscal_year=2024, gender="female",
         location="national", source_name="Global Findex 2024 (via Birr Metrics)",
         source_type="research", source_url="https://birrmetrics.com/49-of-ethiopians-are-banked-as-findex-2025-highlights-the-next-inclusion-challenge/",
         confidence="high", collected_by=COLLECTOR, collection_date=TODAY,
         original_text="only 42 percent of women do",
         notes="Female account ownership, 2024 Findex round"),

    dict(record_id="REC_0037", record_type="observation", pillar="GENDER",
         indicator="Account Ownership Gender Gap", indicator_code="GEN_GAP_ACC",
         indicator_direction="lower_better", value_numeric=15, value_type="gap_pp",
         unit="pp", observation_date="2024-11-29", fiscal_year=2024, gender="all",
         location="national", source_name="Global Findex 2024 (via Birr Metrics)",
         source_type="calculated", source_url="https://birrmetrics.com/49-of-ethiopians-are-banked-as-findex-2025-highlights-the-next-inclusion-challenge/",
         confidence="high", collected_by=COLLECTOR, collection_date=TODAY,
         original_text="a 15-point gap that has not narrowed since the last survey",
         notes="Recomputed 57% male - 42% female = 15pp. Supersedes REC_0028's medium-confidence 18pp estimate; retain both and flag the discrepancy in EDA."),

    dict(record_id="REC_0038", record_type="observation", pillar="USAGE",
         indicator="Digitally Enabled Account Rate", indicator_code="USG_DIGITAL_ENABLED",
         indicator_direction="higher_better", value_numeric=7, value_type="percentage",
         unit="%", observation_date="2024-11-29", fiscal_year=2024, gender="all",
         location="national", source_name="Global Findex 2024 (via Birr Metrics)",
         source_type="research", source_url="https://birrmetrics.com/49-of-ethiopians-are-banked-as-findex-2025-highlights-the-next-inclusion-challenge/",
         confidence="high", collected_by=COLLECTOR, collection_date=TODAY,
         original_text="Only seven percent of adults have digitally enabled accounts",
         notes="New indicator: share of adults with accounts usable for card/phone/app payments. Highlights the access-vs-usage gap central to this challenge."),
]

# ---------- NEW EVENT ----------
new_event = [
    dict(record_id="EVT_0011", record_type="event", category="regulation",
         indicator="Banking Business Proclamation - Foreign Banks Permitted",
         indicator_code="EVT_FOREIGN_BANK", value_text="Enacted",
         value_type="categorical", observation_date="2024-12-17", fiscal_year=2024,
         gender="all", location="national",
         source_name="Ethiopian Parliament / National Law Review",
         source_type="policy",
         source_url="https://natlawreview.com/article/ethiopia-opens-its-banking-sector-foreign-banks-and-investors-after-half-century",
         confidence="high", collected_by=COLLECTOR, collection_date=TODAY,
         original_text="the Ethiopian Parliament approved the new Banking Business law, which allows foreign banks and foreigners to rejoin the Ethiopian market after an absence of half a century",
         notes="NBE began accepting foreign bank license applications June 25, 2025. First major banking-sector liberalization event; not yet captured in dataset."),
]

# ---------- NEW IMPACT LINKS ----------
new_links = [
    dict(record_id="IMP_0015", parent_id="EVT_0011", record_type="impact_link",
         pillar="ACCESS", indicator="Foreign Bank Entry effect on Account Ownership",
         confidence="medium", related_indicator="ACC_OWNERSHIP",
         relationship_type="enabling", impact_direction="increase",
         impact_magnitude="low", impact_estimate=5.0, lag_months=36,
         evidence_basis="theoretical", comparable_country=None,
         collected_by=COLLECTOR, collection_date=TODAY,
         notes="Foreign capital/competition effects on retail account ownership are typically slow; too recent for empirical Ethiopian data."),

    dict(record_id="IMP_0016", parent_id="EVT_0009", record_type="impact_link",
         pillar="ACCESS", indicator="NFIS-II effect on Account Ownership",
         confidence="medium", related_indicator="ACC_OWNERSHIP",
         relationship_type="enabling", impact_direction="increase",
         impact_magnitude="medium", impact_estimate=10.0, lag_months=24,
         evidence_basis="theoretical", comparable_country=None,
         collected_by=COLLECTOR, collection_date=TODAY,
         notes="NFIS-II (2021) previously had no modeled impact_link despite being the umbrella policy with the 70%-by-2025 target. National strategies commonly undershoot targets; flagged as uncertain."),
]

main = pd.concat([main, pd.DataFrame(new_obs), pd.DataFrame(new_event)], ignore_index=True)
impact = pd.concat([impact, pd.DataFrame(new_links)], ignore_index=True)

with pd.ExcelWriter(path, engine="openpyxl") as writer:
    main.to_excel(writer, sheet_name="ethiopia_fi_unified_data", index=False)
    impact.to_excel(writer, sheet_name="Impact_sheet", index=False)

print(f"Added {len(new_obs)} observations, {len(new_event)} event, {len(new_links)} impact_links.")
print(f"New main sheet rows: {len(main)}  |  New impact sheet rows: {len(impact)}")
