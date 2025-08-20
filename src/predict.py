import pandas as pd
import streamlit as st
import joblib
import requests
from io import BytesIO

# ----------------------------
# Load model & training columns dari Google Drive
# ----------------------------
MODEL_URL = "https://drive.google.com/uc?export=download&id=1HDViTPN6WkQpS5dDOHmaEYWCAGgwCJUU"
TRAIN_COLS_URL = "https://drive.google.com/uc?export=download&id=1YOUR_TRAIN_COLS_ID"

@st.cache_data
def load_model_from_gdrive(url):
    r = requests.get(url)
    r.raise_for_status()
    return joblib.load(BytesIO(r.content))

rf = load_model_from_gdrive(MODEL_URL)
training_columns = load_model_from_gdrive(TRAIN_COLS_URL)

# ----------------------------
# Halaman Predict
# ----------------------------
def show_predict_page():
    st.title("🏨 Hotel Cancellation Prediction")
    st.markdown("Isi form berikut untuk memprediksi kemungkinan pembatalan hotel.")

    # ----------------------------
    # Gambar header dari URL online
    # ----------------------------
    img_url = "https://raw.githubusercontent.com/username/repo/main/images/Hotel1.png"
    st.image(img_url, use_container_width=True)

    # ----------------------------
    # Input: 3 kolom
    # ----------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        deposit_type = st.selectbox("Deposit Type", ["Non Refund", "Refundable", "No Deposit"])
        required_car_parking_spaces = st.number_input("Required Car Parking Spaces", 0, 10, 0)
        previous_cancellations = st.number_input("Previous Cancellations", 0, 5, 0)

    with col2:
        market_segment = st.selectbox(
            "Market Segment",
            ["Online TA", "Direct", "Offline TA/TO", "Corporate", "Complementary", "Groups", "Undefined"]
        )
        country = st.selectbox("Country", ["PRT", "ITA", "FRA", "DEU", "AGO", "GBR", "ESP", "CHE", "Other"])
        customer_type = st.selectbox("Customer Type", ["Transient", "Contract", "Group", "Transient-Party"])

    with col3:
        total_of_special_requests = st.number_input("Total of Special Requests", 0, 10, 0)
        reserved_room_type = st.selectbox("Reserved Room Type", ["A", "B", "C", "D", "E", "F", "G", "H", "L"])
        booking_changes = st.number_input("Booking Changes", 0, 5, 0)

    # ----------------------------
    # Slider untuk lead_time & adr
    # ----------------------------
    lead_time = st.slider("Lead Time (days)", 0, 500, 30)
    adr = st.slider("ADR (Average Daily Rate)", 0, 1000, 100)

    # ----------------------------
    # Input untuk adults, children, babies
    # ----------------------------
    adults = st.number_input("Number of Adults", 1, 10, 1)
    children = st.number_input("Number of Children", 0, 5, 0)
    babies = st.number_input("Number of Babies", 0, 5, 0)

    # ----------------------------
    # Buat DataFrame untuk prediksi
    # ----------------------------
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
        "assigned_room_type": reserved_room_type
    }
    input_df = pd.DataFrame([input_dict])

    # One-Hot Encoding agar sesuai training columns
    input_df = pd.get_dummies(input_df)
    for col in training_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[training_columns]

    # ----------------------------
    # Tombol prediksi
    # ----------------------------
    if st.button("Predict"):
        prediction = rf.predict(input_df)[0]
        proba = rf.predict_proba(input_df)[0][1]
        st.success(f"Prediction: {'Canceled' if prediction == 1 else 'Not Canceled'}")
        st.info(f"Probability of cancellation: {proba:.2f}")

    # ----------------------------
    # Input Summary
    # ----------------------------
    if st.button("Show Input Summary", key="summary"):
        st.markdown("### 🧾 Input Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Deposit Type: {deposit_type}")
            st.write(f"Car Parking: {required_car_parking_spaces}")
            st.write(f"Previous Cancellations: {previous_cancellations}")
            st.write(f"Lead Time: {lead_time}")
            st.write(f"ADR: {adr}")
        with col2:
            st.write(f"Market Segment: {market_segment}")
            st.write(f"Country: {country}")
            st.write(f"Customer Type: {customer_type}")
            st.write(f"Adults: {adults}, Children: {children}, Babies: {babies}")
            st.write(f"Reserved Room Type: {reserved_room_type}, Assigned Room Type: {reserved_room_type}")
