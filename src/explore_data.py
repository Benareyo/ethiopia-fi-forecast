import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 150)

# Load datasets
main = pd.read_excel('data/raw/ethiopia_fi_unified_data.xlsx', sheet_name='ethiopia_fi_unified_data')
impact = pd.read_excel('data/raw/ethiopia_fi_unified_data.xlsx', sheet_name='Impact_sheet')

if 'parent_id' not in main.columns:
    main.insert(1, 'parent_id', pd.NA)
impact = impact[main.columns]

data = pd.concat([main, impact], ignore_index=True)
ref = pd.read_excel('data/raw/reference_codes.xlsx', sheet_name='reference_codes')

print("="*60)
print("SHAPE & COLUMNS")
print("="*60)
print(f"Unified data: {data.shape[0]} rows, {data.shape[1]} columns")
print(f"Columns: {list(data.columns)}\n")

print("="*60)
print("RECORD TYPE BREAKDOWN")
print("="*60)
print(data['record_type'].value_counts(), "\n")

print("="*60)
print("PILLAR BREAKDOWN (observations/targets/impact_links only)")
print("="*60)
print(data['pillar'].value_counts(dropna=False), "\n")

print("="*60)
print("SOURCE TYPE BREAKDOWN")
print("="*60)
print(data['source_type'].value_counts(dropna=False), "\n")

print("="*60)
print("CONFIDENCE BREAKDOWN")
print("="*60)
print(data['confidence'].value_counts(dropna=False), "\n")

print("="*60)
print("TEMPORAL RANGE")
print("="*60)
data['observation_date'] = pd.to_datetime(data['observation_date'], errors='coerce')
print(f"Earliest: {data['observation_date'].min()}")
print(f"Latest:   {data['observation_date'].max()}\n")

print("="*60)
print("UNIQUE INDICATORS (indicator_code) + COUNTS")
print("="*60)
print(data[data['record_type']=='observation']['indicator_code'].value_counts(), "\n")

print("="*60)
print("EVENTS CATALOGUED")
print("="*60)
events = data[data['record_type']=='event'][['record_id','indicator','category','observation_date']]
print(events.to_string(index=False), "\n")

print("="*60)
print("IMPACT LINKS SUMMARY (event -> indicator)")
print("="*60)
links = data[data['record_type']=='impact_link'][['parent_id','related_indicator','impact_direction','impact_magnitude','lag_months','evidence_basis']]
print(links.to_string(index=False), "\n")

print("="*60)
print("REFERENCE CODES OVERVIEW")
print("="*60)
print(ref['field'].value_counts())
