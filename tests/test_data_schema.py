import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "ethiopia_fi_unified_data.xlsx")

def load_unified():
    main = pd.read_excel(DATA_PATH, sheet_name="ethiopia_fi_unified_data")
    impact = pd.read_excel(DATA_PATH, sheet_name="Impact_sheet")
    if "parent_id" not in main.columns:
        main.insert(1, "parent_id", pd.NA)
    impact = impact[main.columns]
    return pd.concat([main, impact], ignore_index=True)

def test_file_exists():
    assert os.path.exists(DATA_PATH), "Unified dataset file is missing"

def test_expected_record_types_present():
    data = load_unified()
    types = set(data["record_type"].unique())
    assert {"observation", "event", "target", "impact_link"}.issubset(types)

def test_no_duplicate_record_ids():
    data = load_unified()
    assert data["record_id"].is_unique, "Duplicate record_id found"

def test_impact_links_reference_valid_events():
    data = load_unified()
    event_ids = set(data[data["record_type"] == "event"]["record_id"])
    link_parents = set(data[data["record_type"] == "impact_link"]["parent_id"].dropna())
    missing = link_parents - event_ids
    assert not missing, f"impact_link parent_id(s) with no matching event: {missing}"

def test_observations_have_values():
    data = load_unified()
    obs = data[data["record_type"] == "observation"]
    assert obs["value_numeric"].notna().all(), "Some observations are missing value_numeric"
