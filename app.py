import streamlit as st
import pandas as pd
import plotly.express as px

# Load datasets
df_category = pd.read_csv("cleaned_vahan.csv", parse_dates=["Date"])
df_manufacturer = pd.read_csv("cleaned_vahan_final.csv", parse_dates=["Date"])

# Growth calculations function
def add_growth(df):
    df = df.sort_values(["Category", "Date"])
    df["YoY_Growth"] = df.groupby("Category")["Registrations"].pct_change(periods=12) * 100
    df["QoQ_Growth"] = df.groupby("Category")["Registrations"].pct_change(periods=3) * 100
    return df

df_category = add_growth(df_category)
df_manufacturer = add_growth(df_manufacturer)

st.title("Vahan Vehicle Registrations Dashboard")

# Toggle between Category and Manufacturer
view_option = st.radio("View Mode", ["Vehicle Type", "Manufacturer"], horizontal=True)

# -------------------------------
# Category Mode
# -------------------------------
if view_option == "Vehicle Type":
    categories = st.sidebar.multiselect(
        "Select Vehicle Categories",
        df_category["Category"].unique(),
        default=df_category["Category"].unique()
    )

    date_range = st.sidebar.date_input(
        "Select Date Range",
        [df_category["Date"].min(), df_category["Date"].max()]
    )

    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    mask = (df_category["Category"].isin(categories)) & (df_category["Date"].between(start_date, end_date))
    filtered_df = df_category[mask]

# -------------------------------
# Manufacturer Mode
# -------------------------------
else:
    # Search bar with suggestions
    manufacturer_input = st.text_input("🔍 Search Manufacturer (type to see matches)")
    manufacturer_list = []

    if manufacturer_input:
        matches = [m for m in df_manufacturer["Category"].unique() if manufacturer_input.lower() in m.lower()]
        if matches:
            manufacturer_list = st.multiselect(
                "Select up to 5 manufacturers",
                matches,
                max_selections=5
            )

    date_range = st.sidebar.date_input(
        "Select Date Range",
        [df_manufacturer["Date"].min(), df_manufacturer["Date"].max()]
    )

    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    if manufacturer_list:
        mask = (df_manufacturer["Category"].isin(manufacturer_list)) & (df_manufacturer["Date"].between(start_date, end_date))
        filtered_df = df_manufacturer[mask]
    else:
        filtered_df = df_manufacturer[df_manufacturer["Date"].between(start_date, end_date)]

# -------------------------------
# Growth Toggle
# -------------------------------
growth_option = st.radio(
    "Select Growth Metric",
    ("None", "Year-over-Year Growth (%)", "Quarter-over-Quarter Growth (%)"),
    horizontal=True
)

# -------------------------------
# Chart
# -------------------------------
if not filtered_df.empty:
    if growth_option == "Year-over-Year Growth (%)":
        fig = px.line(filtered_df, x="Date", y="YoY_Growth", color="Category",
                      title="Year-over-Year Growth (%)")
    elif growth_option == "Quarter-over-Quarter Growth (%)":
        fig = px.line(filtered_df, x="Date", y="QoQ_Growth", color="Category",
                      title="Quarter-over-Quarter Growth (%)")
    else:
        fig = px.line(filtered_df, x="Date", y="Registrations", color="Category",
                      title="Monthly Vehicle Registrations")

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for the selected filters.")