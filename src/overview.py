import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import os
from PIL import Image


def plot_outlier(df, column):
    # Pastikan kolom bertipe numerik
    data = pd.to_numeric(df[column], errors='coerce').dropna()

    fig, axes = plt.subplots(1, 3, figsize=(18, 4))

    # Histogram
    sns.histplot(data, bins=30, kde=True, ax=axes[0], color="#6CC38C")
    axes[0].set_title(f"{column} - Histogram")

    # Q-Q Plot
    res = stats.probplot(data, dist="norm", plot=axes[1])
    axes[1].get_lines()[0].set_color("#62996e")  # Data points
    axes[1].get_lines()[1].set_color("#FF6C6C")  # Fitted line
    axes[1].set_title(f"{column} - Q-Q Plot")

    # Boxplot
    sns.boxplot(x=data, ax=axes[2], color="#6CC38C")
    axes[2].set_title(f"{column} - Boxplot")

    st.pyplot(fig)
    plt.clf()


def show_overview():
    # Path file gambar
    image_path = os.path.join(os.path.dirname(__file__), "..", "images", "hotel1.png")
    
    # Cek apakah file ada
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        st.warning("Gambar tidak ditemukan, gunakan gambar default atau URL.")
    
    st.markdown("""
        <div style="background-color: #dee47e; padding: 15px; border-radius: 5px;">
        This dataset contains information on hotel bookings, including booking dates, customer details, and cancellation information.
        </div>
    """, unsafe_allow_html=True)


    st.markdown("### 📦 Dataset Preview")
    st.markdown("Below is a quick glimpse into the hotel booking dataset:")

    df = pd.read_csv("data/cleaned_hotel_data4.csv")
    st.dataframe(df.head(10), use_container_width=True)

    st.markdown("---")

    st.markdown("### 📋 Feature Summary")
    feature_summary = pd.DataFrame({
        "Name": [
            "hotel", "is_canceled", "lead_time", "arrival_date_year", "arrival_date_month",
            "stays_in_weekend_nights", "stays_in_week_nights", "adults", "children",
            "babies", "meal", "country", "market_segment", "distribution_channel",
            "is_repeated_guest", "previous_cancellations", "booking_changes",
            "deposit_type", "agent", "company", "customer_type", "reserved_room_type",
            "assigned_room_type", "booking_time", "total_of_special_requests"
        ],
        "Description": [
            "Type of hotel (City Hotel, Resort Hotel)",
            "Whether the booking was canceled (0=No, 1=Yes)",
            "Number of days between booking and arrival",
            "Year of arrival date",
            "Month of arrival",
            "Number of weekend nights",
            "Number of week nights",
            "Number of adults",
            "Number of children",
            "Number of babies",
            "Type of meal booked",
            "Country of origin of the guest",
            "Market segment designation",
            "Booking distribution channel",
            "Repeated guest flag (0=No, 1=Yes)",
            "Number of previous cancellations",
            "Number of changes made to the booking",
            "Deposit type (No Deposit, Non Refund, Refundable)",
            "Booking agent",
            "Company associated",
            "Customer type (Transient, Group, Contract, Transient-Party)",
            "Reserved room type",
            "Assigned room type",
            "Time of booking",
            "Total number of special requests"
        ]
    })
    st.dataframe(feature_summary, use_container_width=True)

    st.markdown("---")

    st.subheader("📈 Initial Data Overview")

    # Get basic metrics
    total_rows = df.shape[0]
    total_cols = df.shape[1]
    missing_vals = int(df.isnull().sum().sum())

    # Styling with HTML boundaries
    st.markdown("""
    <style>
    .metric-box {
        background-color: #dee47e;
        padding: 15px;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        text-align: center;
    }
    .metric-row {
        display: flex;
        justify-content: space-between;
        gap: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-row">
    <div class="metric-box">
        <h5>📊 Total Rows</h5>
        <p style='font-size: 20px;'>{total_rows}</p>
    </div>
    <div class="metric-box">
        <h5>📐 Total Columns</h5>
        <p style='font-size: 20px;'>{total_cols}</p>
    </div>
    <div class="metric-box">
        <h5>⚠️ Missing Values</h5>
        <p style='font-size: 20px;'>{missing_vals}</p>
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("---")

    with st.expander("🧹 Data Preprocessing Summary"):
        st.subheader("🔎 1. Missing Values")
        missing_data = df.isnull().sum()
        missing_data = missing_data[missing_data > 0]
        st.dataframe(missing_data)

        st.subheader("✅ 2. Duplicate Check")
        if df.duplicated().sum() == 0:
            st.write("No duplicate rows found in the dataset.")
        else:
            st.write(f"Found {df.duplicated().sum()} duplicate rows.")

        st.subheader("📉 3. Outlier Inspection")
        st.markdown("Numerical columns were examined for outliers. Explore below:")

    numeric_cols = ["lead_time", "stays_in_weekend_nights", "stays_in_week_nights", 
                    "adults", "children", "babies", "previous_cancellations",
                    "booking_changes", "total_of_special_requests"]

    for col in numeric_cols:
        with st.expander(f"🧪 Outlier Visualization ({col})"):
            plot_outlier(df, col)



