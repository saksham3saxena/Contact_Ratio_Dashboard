import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# --------------------------------------------------------------------
# 1. LOAD THE CSV DATA
# --------------------------------------------------------------------
@st.cache_data
def load_data():
    # Path to your CSV file
    DATA_FILENAME = Path(__file__).parent / "data/summary_data.csv"
    df = pd.read_csv(DATA_FILENAME)
    
    # Parse the session_date column as datetime, if needed
    df['session_date'] = pd.to_datetime(df['session_date'], errors='coerce')
    
    # Convert numeric columns from string to numeric if necessary
    # (This is only needed if the CSV has them as strings)
    df['CreatedMonth'] = pd.to_numeric(df['CreatedMonth'], errors='coerce',downcast="signed")
    df['CreatedWeek'] = pd.to_numeric(df['CreatedWeek'], errors='coerce',downcast="signed")
    #df['CreatedWeek'] = df['CreatedWeek'].astype(str)
    df['Sum_session_count'] = pd.to_numeric(df['Sum_session_count'], errors='coerce')
    df['Avg_week_txn_counts'] = pd.to_numeric(df['Avg_week_txn_counts'], errors='coerce')
    
    return df

# --------------------------------------------------------------------
# 2. SETUP STREAMLIT APP
# --------------------------------------------------------------------
st.set_page_config(page_title="Week-wise Contact Ratio", layout="wide")
df = load_data()

st.title("Week-wise Contact Ratio Dashboard")

st.markdown("""
Use this dashboard to see how contact ratio changes from **week to week**.
The formula is:

\\[
\\text{Contact Ratio} = 1{,}000{,}000 \\times \\frac{\\text{Sum\\_session\\_count}}{\\text{Avg\\_week\\_txn\\_counts}}
\\]

Below, choose the minimum and maximum week numbers you'd like to analyze.
""")

# --------------------------------------------------------------------
# 3. USER INPUT: WEEK RANGE
# --------------------------------------------------------------------
min_week_in_data = int(df['CreatedWeek'].min())
max_week_in_data = int(df['CreatedWeek'].max())

min_week, max_week = st.slider(
    "Select CreatedWeek range:",
    min_value=min_week_in_data,
    max_value=max_week_in_data,
    value=(min_week_in_data, max_week_in_data)
)

# Filter data by the selected week range
filtered_df = df[(df['CreatedWeek'] >= min_week) & (df['CreatedWeek'] <= max_week)].copy()

# --------------------------------------------------------------------
# 4. CALCULATE CONTACT RATIO
# --------------------------------------------------------------------
# For each row: contact_ratio = 1,000,000 * Sum_session_count / Avg_week_txn_counts
filtered_df['contact_ratio'] = 1_000_000 * (
    filtered_df['Sum_session_count'] / filtered_df['Avg_week_txn_counts']
)

st.subheader("Filtered Results")
st.write("The table below shows rows that fall within the chosen week range, along with the computed contact ratio:")

# Show the results in a table
st.dataframe(filtered_df)

# --------------------------------------------------------------------
# 5. PLOT A CHART OF CONTACT RATIO BY WEEK
# --------------------------------------------------------------------
st.subheader("Contact Ratio by CreatedWeek")

# Sort by CreatedWeek so the chart is in ascending order
filtered_df.sort_values(by='CreatedWeek', inplace=True)

# Plot a line chart
st.line_chart(
    data=filtered_df,
    x='CreatedWeek',
    y='contact_ratio',
    height=400
)

st.markdown("""
**Interpretation:**
- The x-axis represents the `CreatedWeek`.
- The y-axis (contact ratio) is scaled by 1,000,000 to avoid small fractional values.
- This chart helps you visualize how contact ratio changes from one week to another within your selected range.
""")