# Vahan Vehicle Registrations Dashboard

## 📌 Setup Instructions

1.  Clone this repository:

    ``` bash
    git clone https://github.com/Vighnesh-M-S/Automobile_Insights.git
    cd Automobile_Insights
    ```

2.  Install required dependencies:

    ``` bash
    pip install -r requirements.txt
    ```

3.  Place cleaned CSV files inside the project folder:

    -   `cleaned_vahan_final.csv` (Vehicle Type data)
    -   `cleaned_manufacturer_final.csv` (Manufacturer data)

4.  Run the Streamlit app:

    ``` bash
    streamlit run app.py
    ```

------------------------------------------------------------------------

## 📊 Data Assumptions

-   Data is downloaded manually from the **Vahan Dashboard**.
-   Available only **per financial year** and had to be merged across
    years (2021--2025).\
-   Data represents **monthly vehicle registrations** (not revenue).\
-   Only **registrations per vehicle type** and **registrations per
    manufacturer** are considered.\
-   No direct mapping exists between a manufacturer and its category in
    the downloaded format.

------------------------------------------------------------------------

## 🚀 Feature Roadmap (Future Work)

-   **Automatic Data Scraping & Collection**\
    Implement a scheduled scraper to fetch and append new monthly data
    automatically.

-   **Correlation between Manufacturer & Vehicle Type**\
    Currently not possible due to lack of detailed data in Vahan.\
    If such granularity becomes available, we can build insights like:\
    *"Which manufacturer dominates which category (2W, 3W, 4W, EV)?"*

-   **Enhanced Investor Insights**\
    Add market share analysis, trend forecasting, and regional breakdown
    (if data available).

------------------------------------------------------------------------

## 🌐 Deployed Link

\[Deployed Link](https://huggingface.co/spaces/VGreatVig07/Automobile_Insights)

------------------------------------------------------------------------

## 🎥 Explanation Video

[![Video Link](https://github.com/user-attachments/assets/335091be-0113-4b6b-b8d1-73f93f2e2725)](https://youtu.be/VGZElfVpCNg)

------------------------------------------------------------------------

