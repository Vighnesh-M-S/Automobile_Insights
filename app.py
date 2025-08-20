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

st.sidebar.header("Filters")

# ✅ Radio button in sidebar
view_option = st.sidebar.radio("View Mode", ["Vehicle Type", "Manufacturer"])

# Date range filter (common)
if view_option == "Vehicle Type":
    date_range = st.sidebar.date_input(
        "Select Date Range",
        [df_category["Date"].min(), df_category["Date"].max()]
    )
else:
    date_range = st.sidebar.date_input(
        "Select Date Range",
        [df_manufacturer["Date"].min(), df_manufacturer["Date"].max()]
    )

start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

filtered_df = pd.DataFrame()  # start empty

# -------------------------------
# Vehicle Type Mode
# -------------------------------
if view_option == "Vehicle Type":
    categories = st.sidebar.multiselect(
        "Vehicle Types (type to search)",
        options=sorted(df_category["Category"].dropna().astype(str).str.strip().unique()),
        default=[]  # empty until user picks
    )
    if categories:
        mask = (df_category["Category"].isin(categories)) & (df_category["Date"].between(start_date, end_date))
        filtered_df = df_category[mask]

# -------------------------------
# Manufacturer Mode
# -------------------------------
else:
    manufacturers = sorted(df_manufacturer["Category"].dropna().astype(str).str.strip().unique())

    selected_manu = st.sidebar.multiselect(
        "Manufacturers (type to search, pick up to 5)",
        options=manufacturers,
        default=[],  # empty until user picks
        # If your Streamlit version supports it, uncomment the next line:
        # max_selections=5
    )

    # Fallback cap if your Streamlit version doesn’t support max_selections
    if len(selected_manu) > 5:
        st.sidebar.warning("Select up to 5 manufacturers. Using the first 5 you picked.")
        selected_manu = selected_manu[:5]

    if selected_manu:
        mask = (df_manufacturer["Category"].isin(selected_manu)) & (df_manufacturer["Date"].between(start_date, end_date))
        filtered_df = df_manufacturer[mask]

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

    st.markdown("---")  # separator

    st.subheader("📌 Key Insights")

    # Total registrations
    total_reg = filtered_df["Registrations"].sum()

    # Group by Category/Manufacturer for rankings
    grouped = filtered_df.groupby("Category")["Registrations"].sum().reset_index()

    # Best performer
    best = grouped.loc[grouped["Registrations"].idxmax()]
    best_cat, best_val = best["Category"], best["Registrations"]

    # Worst performer
    worst = grouped.loc[grouped["Registrations"].idxmin()]
    worst_cat, worst_val = worst["Category"], worst["Registrations"]

    # Avg YoY growth (if column exists)
    avg_yoy = filtered_df["YoY_Growth"].mean(skipna=True)

    # Show metrics in 4 columns
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Registrations", f"{total_reg:,}")
    col2.metric("Top Performer", best_cat, f"{best_val:,}")
    col3.metric("Lowest Performer", worst_cat, f"{worst_val:,}")
    col4.metric("Avg YoY Growth", f"{avg_yoy:.2f}%")

    
else:
    st.info("👆 Choose at least one Vehicle Type or Manufacturer to see results.")