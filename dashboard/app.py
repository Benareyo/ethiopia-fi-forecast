"""
Ethiopia Financial Inclusion Forecasting Dashboard
Selam Analytics | Task 5

Run locally with:
    streamlit run dashboard/app.py
(run from the repo root so the relative data paths resolve correctly)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os

st.set_page_config(page_title="Ethiopia Financial Inclusion Dashboard", layout="wide")

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@st.cache_data
def load_data():
    data_path = os.path.join(BASE_DIR, "data", "raw", "ethiopia_fi_unified_data.xlsx")
    main = pd.read_excel(data_path, sheet_name="ethiopia_fi_unified_data")
    impact = pd.read_excel(data_path, sheet_name="Impact_sheet")
    if "parent_id" not in main.columns:
        main.insert(1, "parent_id", pd.NA)
    impact = impact[main.columns]
    data = pd.concat([main, impact], ignore_index=True)
    data["observation_date"] = pd.to_datetime(data["observation_date"], errors="coerce")
    return data

@st.cache_data
def load_forecast():
    path = os.path.join(BASE_DIR, "data", "processed", "forecast_table.csv")
    if os.path.exists(path):
        return pd.read_csv(path, index_col="Year")
    return None

@st.cache_data
def load_impact_matrix():
    path = os.path.join(BASE_DIR, "data", "processed", "event_impact_matrix.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

data = load_data()
forecast_df = load_forecast()
impact_matrix = load_impact_matrix()

obs = data[data["record_type"] == "observation"].copy()
obs["year"] = obs["observation_date"].dt.year
events = data[data["record_type"] == "event"].copy()

# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
st.sidebar.title("Ethiopia Financial Inclusion")
page = st.sidebar.radio("Navigate", ["Overview", "Trends", "Forecasts", "Inclusion Projections"])
st.sidebar.markdown("---")
st.sidebar.caption("Selam Analytics | Forecasting Financial Inclusion in Ethiopia")

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------
def get_indicator_series(code, gender="all", location="national"):
    sub = obs[obs["indicator_code"] == code]
    if "gender" in sub.columns and gender is not None:
        g = sub[sub["gender"] == gender]
        if len(g) > 0:
            sub = g
    if "location" in sub.columns and location is not None:
        l = sub[sub["location"] == location]
        if len(l) > 0:
            sub = l
    return sub.sort_values("year")

acc = get_indicator_series("ACC_OWNERSHIP")
usg = get_indicator_series("USG_DIGITAL_PAYMENT")

# ===========================================================================
# PAGE: OVERVIEW
# ===========================================================================
if page == "Overview":
    st.title("Overview")
    st.caption("Key metrics summary for Ethiopia's financial inclusion trajectory")

    col1, col2, col3, col4 = st.columns(4)
    latest_acc = acc.iloc[-1]["value_numeric"] if len(acc) else np.nan
    prev_acc = acc.iloc[-2]["value_numeric"] if len(acc) > 1 else np.nan
    latest_usg = usg.iloc[-1]["value_numeric"] if len(usg) else np.nan
    prev_usg = usg.iloc[-2]["value_numeric"] if len(usg) > 1 else np.nan

    col1.metric("Account Ownership (2024)", f"{latest_acc:.0f}%",
                f"+{latest_acc - prev_acc:.0f}pp vs 2021" if not np.isnan(prev_acc) else None)
    col2.metric("Digital Payment Adoption (2024)", f"{latest_usg:.0f}%",
                f"+{latest_usg - prev_usg:.0f}pp vs 2021" if not np.isnan(prev_usg) else None)

    mm = get_indicator_series("ACC_MM_ACCOUNT")
    if len(mm):
        col3.metric("Mobile Money Accounts (2024)", f"{mm.iloc[-1]['value_numeric']:.2f}%")

    p2p = obs[obs["indicator_code"] == "USG_P2P_COUNT"].sort_values("year")
    atm = obs[obs["indicator_code"] == "USG_ATM_COUNT"].sort_values("year")
    if len(p2p) and len(atm):
        ratio = p2p.iloc[-1]["value_numeric"] / atm.iloc[-1]["value_numeric"]
        col4.metric("P2P / ATM Crossover Ratio", f"{ratio:.2f}x",
                    "P2P now exceeds ATM volume" if ratio > 1 else "ATM still leads")

    st.markdown("---")
    st.subheader("Growth Rate Highlights")
    growth_col1, growth_col2 = st.columns(2)
    with growth_col1:
        if len(acc) > 1:
            acc_growth = acc.copy()
            acc_growth["pp_change"] = acc_growth["value_numeric"].diff()
            acc_growth["years_elapsed"] = acc_growth["year"].diff()
            acc_growth["pp_per_year"] = acc_growth["pp_change"] / acc_growth["years_elapsed"]
            fig = px.bar(acc_growth.dropna(subset=["pp_per_year"]), x="year", y="pp_per_year",
                         title="Account Ownership Growth Rate (pp/year)",
                         labels={"pp_per_year": "pp per year", "year": "Survey Year"})
            st.plotly_chart(fig, use_container_width=True)
    with growth_col2:
        st.markdown("**Why growth decelerated (2021-2024):**")
        st.write(
            "Account ownership grew only +3pp despite massive mobile money "
            "expansion. Key factors: (1) many new mobile money accounts "
            "belonged to people who already had bank accounts, (2) only 66% "
            "of registered M-Pesa accounts are 90-day active, and (3) the "
            "2024 survey excluded regions representing ~30% of the population, "
            "adding uncertainty to the comparison."
        )

    st.markdown("---")
    st.subheader("Business Questions This Dashboard Answers")
    st.markdown("""
    1. **What drives financial inclusion in Ethiopia?** See *Trends* for event overlays and *Forecasts* for modeled event effects.
    2. **How do events affect inclusion outcomes?** See the Event-Indicator Impact Matrix below.
    3. **How will inclusion evolve through 2027?** See *Inclusion Projections*.
    """)

    if impact_matrix is not None:
        st.subheader("Event-Indicator Impact Matrix")
        pivot = impact_matrix.pivot_table(index="event_name", columns="related_indicator",
                                            values="refined_effect_pp", aggfunc="first")
        fig = px.imshow(pivot, color_continuous_scale="RdBu_r", color_continuous_midpoint=0,
                         aspect="auto", text_auto=".1f",
                         labels=dict(color="Effect (pp)"))
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

# ===========================================================================
# PAGE: TRENDS
# ===========================================================================
elif page == "Trends":
    st.title("Trends")
    st.caption("Interactive time series exploration")

    indicator_options = sorted(obs["indicator_code"].dropna().unique())
    default_idx = indicator_options.index("ACC_OWNERSHIP") if "ACC_OWNERSHIP" in indicator_options else 0
    selected_indicators = st.multiselect("Select indicator(s) to compare",
                                          indicator_options, default=[indicator_options[default_idx]])

    year_min, year_max = int(obs["year"].min()), int(obs["year"].max())
    date_range = st.slider("Date range", year_min, year_max, (year_min, year_max))

    if selected_indicators:
        fig = go.Figure()
        for ind in selected_indicators:
            sub = obs[(obs["indicator_code"] == ind) &
                      (obs["year"] >= date_range[0]) & (obs["year"] <= date_range[1])]
            if "gender" in sub.columns:
                sub = sub[(sub["gender"] == "all") | (sub["gender"].isna())]
            sub = sub.sort_values("year")
            if len(sub):
                fig.add_trace(go.Scatter(x=sub["year"], y=sub["value_numeric"],
                                          mode="lines+markers", name=ind))
        fig.update_layout(title="Indicator Trends", xaxis_title="Year", yaxis_title="Value",
                           height=500)
        st.plotly_chart(fig, use_container_width=True)

        csv = obs[obs["indicator_code"].isin(selected_indicators)].to_csv(index=False)
        st.download_button("Download this data as CSV", csv, "indicator_trends.csv", "text/csv")
    else:
        st.info("Select at least one indicator above.")

    st.markdown("---")
    st.subheader("Channel Comparison: P2P vs ATM")
    p2p = obs[obs["indicator_code"] == "USG_P2P_COUNT"].sort_values("year")
    atm = obs[obs["indicator_code"] == "USG_ATM_COUNT"].sort_values("year")
    if len(p2p) or len(atm):
        combined = pd.concat([
            p2p.assign(channel="P2P Transfers"),
            atm.assign(channel="ATM Withdrawals")
        ])
        fig2 = px.bar(combined, x="year", y="value_numeric", color="channel", barmode="group",
                      labels={"value_numeric": "Transaction Count", "year": "Fiscal Year"})
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("Event Timeline")
    events_sorted = events.sort_values("observation_date")
    fig3 = px.scatter(events_sorted, x="observation_date", y=[1]*len(events_sorted),
                       hover_name="indicator", hover_data={"category": True},
                       labels={"observation_date": "Date"})
    fig3.update_traces(marker=dict(size=14))
    fig3.update_yaxes(visible=False)
    fig3.update_layout(height=250, title="Cataloged Events")
    st.plotly_chart(fig3, use_container_width=True)

# ===========================================================================
# PAGE: FORECASTS
# ===========================================================================
elif page == "Forecasts":
    st.title("Forecasts")
    st.caption("Access and Usage projections, 2025-2027")

    if forecast_df is None:
        st.warning("Forecast data not found. Run notebooks/04_forecasting.ipynb first to generate "
                   "data/processed/forecast_table.csv.")
    else:
        model_choice = st.selectbox("Select forecast dimension", ["Access (Account Ownership)",
                                                                     "Usage (Digital Payments)"])
        prefix = "Access" if "Access" in model_choice else "Usage"

        fig = go.Figure()
        years = forecast_df.index.tolist()
        fig.add_trace(go.Scatter(x=years, y=forecast_df[f"{prefix} - Base"],
                                  mode="lines+markers", name="Base case", line=dict(color="#4C72B0")))
        fig.add_trace(go.Scatter(x=years, y=forecast_df[f"{prefix} - Optimistic"],
                                  mode="lines", name="Optimistic", line=dict(dash="dash", color="#55A868")))
        fig.add_trace(go.Scatter(x=years, y=forecast_df[f"{prefix} - Pessimistic"],
                                  mode="lines", name="Pessimistic", line=dict(dash="dash", color="#C44E52"),
                                  fill="tonexty", fillcolor="rgba(76,114,176,0.1)"))
        fig.update_layout(title=f"{model_choice} Forecast with Scenario Range",
                           xaxis_title="Year", yaxis_title="%", height=500)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Forecast Table")
        display_cols = [c for c in forecast_df.columns if prefix in c]
        st.dataframe(forecast_df[display_cols].round(1), use_container_width=True)

        csv = forecast_df.to_csv().encode("utf-8")
        st.download_button("Download full forecast table (CSV)", csv, "forecast_table.csv", "text/csv")

        st.markdown("---")
        st.subheader("Key Projected Milestones")
        base_2027 = forecast_df.loc[2027, f"{prefix} - Base"]
        st.write(f"- Base case projects **{base_2027:.1f}%** by 2027")
        st.write(f"- Optimistic case: **{forecast_df.loc[2027, f'{prefix} - Optimistic']:.1f}%** by 2027")
        st.write(f"- Pessimistic case: **{forecast_df.loc[2027, f'{prefix} - Pessimistic']:.1f}%** by 2027")

        st.info(
            "Methodology: linear trend baseline + S-curve event effects (Task 3), "
            "dampened using a calibration factor derived from validating against "
            "the one real before/after case (M-Pesa launch \u2192 mobile money accounts). "
            "See notebooks/03_impact_modeling.ipynb and 04_forecasting.ipynb for full detail."
        )

# ===========================================================================
# PAGE: INCLUSION PROJECTIONS
# ===========================================================================
elif page == "Inclusion Projections":
    st.title("Inclusion Projections")
    st.caption("Progress toward national targets, with scenario selection")

    scenario = st.selectbox("Scenario", ["Pessimistic", "Base", "Optimistic"])

    if forecast_df is not None:
        acc_col = f"Access - {scenario}"
        usg_col = f"Usage - {scenario}"

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Progress Toward 60% Access Target")
            proj_2027 = forecast_df.loc[2027, acc_col]
            progress = min(proj_2027 / 60 * 100, 100)
            st.progress(progress / 100)
            st.write(f"Projected 2027 Access ({scenario}): **{proj_2027:.1f}%** "
                     f"({progress:.0f}% of the way to a 60% milestone)")

        with col2:
            st.subheader("NFIS-II Target Comparison")
            target_2025 = 70
            proj_2025 = forecast_df.loc[2025, acc_col]
            gap = target_2025 - proj_2025
            st.metric("2025 Access Projection", f"{proj_2025:.1f}%",
                       f"{-gap:.1f}pp vs 70% target", delta_color="inverse")

        st.markdown("---")
        st.subheader("Full Projection, All Scenarios")
        fig = go.Figure()
        for sc, color in [("Pessimistic", "#C44E52"), ("Base", "#4C72B0"), ("Optimistic", "#55A868")]:
            fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df[f"Access - {sc}"],
                                      mode="lines+markers", name=f"Access ({sc})",
                                      line=dict(color=color)))
        fig.add_hline(y=70, line_dash="dot", line_color="gray",
                       annotation_text="NFIS-II 70% target (2025)")
        fig.update_layout(title="Access Projections vs. NFIS-II Target", height=450)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("Answers to the Consortium's Key Questions")
        st.markdown(f"""
        **What drives financial inclusion in Ethiopia?**
        Product launches (Telebirr, M-Pesa) and identity infrastructure (Fayda ID) show the
        largest modeled effects on Access, but real-world growth has consistently underperformed
        naive event-based estimates \u2014 by a factor of roughly 5.8x based on the one validated
        case. Usage growth appears more responsive to events than Access.

        **How do events affect outcomes?**
        See the Event-Indicator Impact Matrix on the Overview page. Effects build gradually
        (S-curve), not instantly, over 3-36 months depending on the event.

        **How will inclusion evolve through 2027?**
        {scenario} scenario: Access reaches **{forecast_df.loc[2027, acc_col]:.1f}%** and Usage
        reaches **{forecast_df.loc[2027, usg_col]:.1f}%** by 2027 \u2014 continued gradual progress,
        not the acceleration the NFIS-II targets assumed.
        """)
    else:
        st.warning("Forecast data not found. Run the Task 4 notebook first.")

st.sidebar.markdown("---")
st.sidebar.caption("Data as of the 2024 Global Findex round. See reports/ for full methodology.")
