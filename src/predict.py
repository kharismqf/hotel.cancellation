import pandas as pd
import streamlit as st
import joblib
import requests
from io import BytesIO
from pathlib import Path

# -----------------------------
# LINK GOOGLE DRIVE
# -----------------------------
MODEL_URL = "https://drive.google.com/uc?export=download&id=1HDViTPN6WkQpS5dDOHmaEYWCAGgwCJUU"
TRAIN_COLS_URL = "https://drive.google.com/uc?export=download&id=14tmlc4z7ZHbYxePdV9cLyO5OHtqAO9cf"

# -----------------------------
# Fungsi untuk load model dari Drive
# -----------------------------
@st.cache_data
def load_model_from_gdrive(url):
    r = requests.get(url)
    r.raise_for_status()  # cek kalau ada error
    return joblib.load(BytesIO(r.content))

# -----------------------------
# Load model & training columns
# -----------------------------
rf = load_model_from_gdrive(MODEL_URL)
training_columns = load_model_from_gdrive(TRAIN_COLS_URL)

# -----------------------------
# Halaman Predict
# -----------------------------
def show_predict_page():
    st.title("Hotel Cancellation Prediction")
    st.markdown("Isi form berikut untuk memprediksi kemungkinan pembatalan hotel.")

    # -----------------------------
    # Gambar Hotel di sebelah kiri
    # -----------------------------
    img_path = Path(__file__).parent.parent / "images" / "hotel2.png"
    img_col, form_col = st.columns([1, 3])
    with img_col:
        st.image(str(img_path), use_container_width=True)

    # -----------------------------
    # Input form 3 kolom
    # -----------------------------
    with form_col:
        col1, col2, col3 = st.columns(3)
        with col1:
            deposit_type = st.selectbox("Deposit Type", ["Non Refund", "Refundable", "No Deposit"])
            required_car_parking_spaces = st.number_input("Car Parking Spaces", 0, 10, 0)
            previous_cancellations = st.number_input("Previous Cancellations", 0, 10, 0)

        with col2:
            market_segment = st.selectbox("Market Segment", ["Online TA", "Direct", "Offline TA/TO", "Corporate", "Complementary", "Groups", "Undefined"])
            country = st.selectbox("Country", ["PRT","ITA","FRA","DEU","AGO","GBR","ESP","CHE","Other"])
            customer_type = st.selectbox("Customer Type", ["Transient","Contract","Group","Transient-Party"])

        with col3:
            total_of_special_requests = st.number_input("Special Requests", 0, 10, 0)
            reserved_room_type = st.selectbox("Reserved Room Type", ["A","B","C","D","E","F","G","H","L"])
            booking_changes = st.number_input("Booking Changes", 0, 10, 0)

        # -----------------------------
        # Slider lead_time & ADR bersebelahan
        # -----------------------------
        col4, col5 = st.columns(2)
        with col4:
            lead_time = st.slider("Lead Time (days)", 0, 500, 30)
        with col5:
            adr = st.slider("ADR", 0, 1000, 100)

        # -----------------------------
        # Adults, Children, Babies 3 kolom
        # -----------------------------
        col6, col7, col8 = st.columns(3)
        with col6:
            adults = st.number_input("Adults", 1, 10, 1)
        with col7:
            children = st.number_input("Children", 0, 5, 0)
        with col8:
            babies = st.number_input("Babies", 0, 5, 0)

    # -----------------------------
    # Buat DataFrame untuk prediksi
    # -----------------------------
    input_dict = {
        "deposit_type": deposit_type,
        "market_segment": market_segment,
        "required_car_parking_spaces": required_car_parking_spaces,
        "country": country,
        "customer_type": customer_type,
        "previous_cancellations": previous_cancellations,
        "lead_time": lead_time,
        "adults": adults,
        "children": children,
        "babies": babies,
        "adr": adr,
        "total_of_special_requests": total_of_special_requests,
        "reserved_room_type": reserved_room_type,
        "booking_changes": booking_changes,
        "assigned_room_type": reserved_room_type  # default sama reserved
    }
    input_df = pd.DataFrame([input_dict])

    # One-Hot Encoding
    input_df = pd.get_dummies(input_df)
    for col in set(training_columns) - set(input_df.columns):
        input_df[col] = 0
    input_df = input_df[training_columns]

    # -----------------------------
    # Tombol Predict
    # -----------------------------
    if st.button("Predict", key="predict_button"):
        prediction = rf.predict(input_df)[0]
        proba = rf.predict_proba(input_df)[0][1]
        st.success(f"Prediction: {'Canceled' if prediction==1 else 'Not Canceled'}")

        # 🔍 Input Summary
        st.markdown("### 🧾 Input Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**🏨 Deposit Type:** {deposit_type}")
            st.markdown(f"**📦 Car Parking Spaces:** {required_car_parking_spaces}")
            st.markdown(f"**❌ Previous Cancellations:** {previous_cancellations}")
            st.markdown(f"**⏳ Lead Time:** {lead_time}")
            st.markdown(f"**💰 ADR:** {adr}")
        with col2:
            st.markdown(f"**🌐 Market Segment:** {market_segment}")
            st.markdown(f"**🌍 Country:** {country}")
            st.markdown(f"**👤 Customer Type:** {customer_type}")
            st.markdown(f"**👨‍👩‍👧‍👦 Adults:** {adults}, Children: {children}, Babies: {babies}")
            st.markdown(f"**🛏️ Reserved Room Type:** {reserved_room_type}, Assigned Room Type:** {reserved_room_type}")


