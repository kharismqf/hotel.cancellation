import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# ---------------------------
# Load Data
# ---------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/cleaned_hotel_data4.csv")
        return df
    except Exception as e:
        st.error(f"❌ Error loading dataset: {e}")
        return pd.DataFrame()


# ---------------------------
# EDA Page
# ---------------------------
def show_eda():
    st.title("🔍 Exploratory Data Analysis - Hotel Cancellation")
    df = load_data()

    if df.empty:
        st.warning("❌ Dataset is empty after loading. Please check the CSV or path.")
        return

    # Section 1 - Preview
    st.header("📋 Dataset Preview")
    st.dataframe(df.head())
    st.divider()

    # Section 2 - Numerical Feature Distribution
    st.header("📈 Numerical Feature Distribution")
    numerical_cols = [
        'lead_time', 'stays_in_weekend_nights', 'stays_in_week_nights',
        'adults', 'children', 'babies', 'previous_cancellations',
        'booking_changes', 'total_of_special_requests'
    ]

    if numerical_cols:
        selected_num = st.selectbox("Select a numerical column:", numerical_cols)
        fig = px.histogram(
            df,
            x=selected_num,
            nbins=30,
            marginal="box",
            title=f"Distribution of {selected_num}"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("🔎 No numerical columns found.")

    st.subheader("📊 Categorical Feature Analysis")
    cat_cols = [
        'hotel', 'market_segment', 'deposit_type', 'customer_type',
        'reserved_room_type', 'assigned_room_type'
    ]

    selected_cat = st.selectbox("🔎 Pilih kolom kategorikal untuk dieksplorasi:", cat_cols)
    fig = px.histogram(
        df,
        x=selected_cat,
        color_discrete_sequence=["#95DCE2"],
        text_auto=True,
        category_orders={selected_cat: sorted(df[selected_cat].unique())},
        labels={selected_cat: selected_cat},
    )
    fig.update_layout(
        title=f"Distribusi dari '{selected_cat}'",
        xaxis_title=selected_cat,
        yaxis_title="Jumlah",
        bargap=0.15
    )
    fig.update_traces(marker_line_width=1, opacity=0.85)
    st.plotly_chart(fig, use_container_width=True)

    st.header("🤔 Insightful Questions")
    st.divider()

    # Section 3 - Cancellation Rate by Hotel Type
    st.subheader("1️⃣ Cancellation Rate by Hotel Type")
    if 'hotel' in df.columns and 'is_canceled' in df.columns:
        cancel_rate = df.groupby('hotel')['is_canceled'].mean().reset_index()
        # ambil top 10 hotel dengan cancel rate tertinggi
        cancel_rate = cancel_rate.sort_values(by='is_canceled', ascending=False).head(10)
        # format text 3 desimal
        cancel_rate['is_canceled_text'] = cancel_rate['is_canceled'].apply(lambda x: f"{x:.3f}")
        
        fig = px.bar(
            cancel_rate,
            x='hotel',
            y='is_canceled',
            text='is_canceled_text',
            title="Top 10 Hotels by Cancellation Rate",
            labels={'is_canceled': 'Cancellation Rate'}
        )
        st.plotly_chart(fig, use_container_width=True)
    st.divider()

    # Section 4 - Market Segment vs Cancellation
    st.subheader("2️⃣ Market Segment vs Cancellation")
    if 'market_segment' in df.columns and 'is_canceled' in df.columns:
        segment_cancel = df.groupby('market_segment')['is_canceled'].mean().reset_index()
        # format 3 desimal untuk text
        segment_cancel['is_canceled_text'] = segment_cancel['is_canceled'].apply(lambda x: f"{x:.3f}")
        
        fig = px.bar(
            segment_cancel,
            x='market_segment',
            y='is_canceled',
            text='is_canceled_text',
            title="Cancellation Rate by Market Segment"
        )
        st.plotly_chart(fig, use_container_width=True)
    st.divider()

    # Section 5 - Deposit Type vs Cancellation
    st.subheader("3️⃣ Deposit Type vs Cancellation")
    if 'deposit_type' in df.columns and 'is_canceled' in df.columns:
        deposit_cancel = df.groupby('deposit_type')['is_canceled'].mean().reset_index()
        deposit_cancel['is_canceled_text'] = deposit_cancel['is_canceled'].apply(lambda x: f"{x:.3f}")
        
        fig = px.bar(
            deposit_cancel,
            x='deposit_type',
            y='is_canceled',
            text='is_canceled_text',
            title="Cancellation Rate by Deposit Type"
        )
        st.plotly_chart(fig, use_container_width=True)
    st.divider()


    # Section 6 - Special Requests vs Cancellation
    st.subheader("4️⃣ Special Requests vs Cancellation")
    if 'total_of_special_requests' in df.columns and 'is_canceled' in df.columns:
        fig, ax = plt.subplots()
        sns.boxplot(data=df, x='is_canceled', y='total_of_special_requests', ax=ax)
        ax.set_xlabel("Canceled")
        ax.set_ylabel("Total Special Requests")
        st.pyplot(fig)
    st.divider()

    # Section 7 - Monthly Customer & Booking Trend
    # Bisa menggunakan arrival_date_year dan arrival_date_month
    df['month_year'] = pd.to_datetime(df['arrival_date_year'].astype(str) + '-' + df['arrival_date_month'].astype(str))

    # Lalu baru bisa groupby
    monthly_summary = df.groupby('month_year').agg({
        'hotel': 'count',                # jumlah booking
        'is_canceled': 'mean'            # rata-rata cancellation
    }).reset_index()

    # Jika belum ada, buat kolom numeric
    df['canceled_numeric'] = df['is_canceled'].astype(int)

    # Atau langsung pakai 'is_canceled' untuk mean
    monthly_summary = df.groupby('month_year').agg(
        total_customers=('total_of_special_requests', 'count'),  # bisa diganti kolom customer unik jika ada
        total_bookings=('is_canceled', 'count'),
        avg_cancellation=('is_canceled', 'mean')  # pakai langsung is_canceled
    ).reset_index()


    st.subheader("5️⃣ Monthly Customer & Booking Trend")
    monthly_summary = df.groupby('month_year').agg(
        total_customers=('total_of_special_requests', 'count'),  # bisa diganti kolom customer unik jika ada
        total_bookings=('is_canceled', 'count'),
        avg_cancellation=('canceled_numeric', 'mean')
    ).reset_index()
    
    # Plot area chart untuk customer & booking
    fig = px.area(
        monthly_summary, 
        x='month_year', 
        y=['total_customers','total_bookings'],
        labels={'value':'Jumlah','month_year':'Bulan'},
        title="Monthly Booking Trend Overview"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Plot avg cancellation line
    fig2 = px.line(
        monthly_summary,
        x='month_year',
        y='avg_cancellation',
        labels={'avg_cancellation':'Avg Cancellation'},
        title="Average Cancellation Rate per Month"
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.divider()


    # Section 8 - ADR vs Month & Customer Count
    st.subheader("6️⃣ ADR vs Month & Customer Count")
    adr_summary = df.groupby('month_year').agg(
        avg_adr=('adr', 'mean'),
        total_customers=('total_of_special_requests', 'count')  # bisa diganti sesuai kolom customer
    ).reset_index()

    fig = px.bar(
        adr_summary, 
        x='month_year', 
        y='avg_adr', 
        color='total_customers', 
        labels={'avg_adr':'Average Daily Rate','month_year':'Bulan','total_customers':'Jumlah Customer'},
        title="Monthly ADR Trend Overview"
    )
    st.plotly_chart(fig, use_container_width=True)