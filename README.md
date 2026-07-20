## Running the Dashboard

The dashboard requires the Task 3 and Task 4 notebooks to have been run at least once, since it reads their outputs (`data/processed/event_impact_matrix.csv` and `data/processed/forecast_table.csv`).

1. Install dependencies (from the repo root):
   ```
   pip install -r requirements.txt
   ```

2. Run the Task 3 and Task 4 notebooks once (via VS Code "Run All", or):
   ```
   jupyter nbconvert --to notebook --execute --inplace notebooks/03_impact_modeling.ipynb
   jupyter nbconvert --to notebook --execute --inplace notebooks/04_forecasting.ipynb
   ```

3. Launch the dashboard from the repo root (not from inside `dashboard/`):
   ```
   streamlit run dashboard/app.py
   ```

4. Your browser should open automatically to `http://localhost:8501`. If not, open that URL manually.

### Dashboard pages
- **Overview** — key metric cards, P2P/ATM crossover ratio, growth rate highlights, event-indicator impact matrix
- **Trends** — interactive time series with indicator selector, date range slider, channel comparison, CSV download
- **Forecasts** — Access/Usage scenario forecasts with confidence bands, forecast table, CSV download
- **Inclusion Projections** — progress toward the 60% milestone and NFIS-II 70% target, scenario selector, answers to the consortium's three key questions
