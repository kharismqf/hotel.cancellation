import pandas as pd
import streamlit as st
import joblib
import requests
from io import BytesIO

# ----------------------------
# LINK GOOGLE DRIVE
# ----------------------------
# Ganti FILE_ID dengan ID asli dari file Google Drive kamu
MODEL_URL = "https://drive.google.com/uc?export=download&id=1HDViTPN6WkQpS5dDOHmaEYWCAGgwCJUU"
TRAIN_COLS_URL = "https://drive.google.com/uc?export=download&id=14tmlc4z7ZHbYxePdV9cLyO5OHtqAO9cf"  # Ganti ini

# ----------------------------
# Fungsi untuk load model dari Drive
# ----------------------------
@st.cache_data
def load_model_from_gdrive(url):
    r = requests.get(url)
    r.raise_for_status()  # cek kalau ada error
    return joblib.load(BytesIO(r.content))

# Load model & training columns
rf = load_model_from_gdrive(MODEL_URL)
training_columns = load_model_from_gdrive(14tmlc4z7ZHbYxePdV9cLyO5OHtqAO9cf)

# ----------------------------
# Halaman Predict
# ----------------------------
def show_predict_page():
    st.title("Hotel Cancellation Prediction")
    st.markdown("Isi form berikut untuk memprediksi kemungkinan pembatalan hotel.")

    # Input form
    lead_time = st.slider("Lead Time (days)", 0, 500, 30)
    adr = st.slider("ADR", 0, 1000, 100)
    adults = st.number_input("Adults", 1, 10, 1)
    children = st.number_input("Children", 0, 5, 0)
    babies = st.number_input("Babies", 0, 5, 0)
    deposit_type = st.selectbox("Deposit Type", ["Non Refund", "Refundable", "No Deposit"])
    market_segment = st.selectbox("Market Segment", ["Online TA", "Direct", "Offline TA/TO", "Corporate", "Complementary", "Groups", "Undefined"])

    # Buat dict dan DataFrame
    input_dict = {
        "lead_time": lead_time,
        "adr": adr,
        "adults": adults,
        "children": children,
        "babies": babies,
        "deposit_type": deposit_type,
        "market_segment": market_segment,
    }
    input_df = pd.DataFrame([input_dict])

    # One-Hot Encoding
    input_df = pd.get_dummies(input_df)
    missing_cols = set(training_columns) - set(input_df.columns)
    for col in missing_cols:
        input_df[col] = 0
    input_df = input_df[training_columns]

    if st.button("Predict"):
        prediction = rf.predict(input_df)[0]
        proba = rf.predict_proba(input_df)[0][1]
        st.success(f"Prediction: {'Canceled' if prediction == 1 else 'Not Canceled'}")
        st.info(f"Probability of cancellation: {proba:.2f}")
