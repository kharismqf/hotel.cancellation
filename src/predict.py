import pandas as pd
import streamlit as st
import joblib
import requests
from io import BytesIO

# -----------------------------
# Fungsi untuk download model dari Google Drive
# -----------------------------
def download_model_from_gdrive(file_id):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    response.raise_for_status()
    return BytesIO(response.content)

# -----------------------------
# Load model & training columns
# -----------------------------
model_file_id = "1HDViTPN6WkQpS5dDOHmaEYWCAGgwCJUU"  # ID file rf_model_20pct.pkl
training_columns_file_id = "1HDViTPN6WkQpS5dDOHmaEYWCAGgwCJUU"      # ID file training_columns_20pct.pkl

with st.spinner("Loading model..."):
    rf = joblib.load(download_model_from_gdrive(model_file_id))
    training_columns = joblib.load(download_model_from_gdrive(training_columns_file_id))

# -----------------------------
# Streamlit Page
# -----------------------------
def show_predict_page():
    st.title("Hotel Cancellation Prediction")
    st.markdown("Isi form berikut untuk memprediksi kemungkinan pembatalan hotel.")

    # -----------------------------
    # Input user
    # -----------------------------
    lead_time = st.slider("Lead Time (days)", 0, 500, 30)
    adr = st.slider("ADR", 0, 1000, 100)
    adults = st.number_input("Adults", 1, 10, 1)
    children = st.number_input("Children", 0, 5, 0)
    babies = st.number_input("Babies", 0, 5, 0)
    deposit_type = st.selectbox("Deposit Type", ["Non Refund", "Refundable", "No Deposit"])
    market_segment = st.selectbox("Market Segment", ["Online TA", "Direct", "Offline TA/TO", "Corporate", "Complementary", "Groups", "Undefined"])

    # -----------------------------
    # Buat DataFrame & OHE
    # -----------------------------
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
    input_df = pd.get_dummies(input_df)
    missing_cols = set(training_columns) - set(input_df.columns)
    for col in missing_cols:
        input_df[col] = 0
    input_df = input_df[training_columns]

    # -----------------------------
    # Tombol Prediksi
    # -----------------------------
    if st.button("Predict"):
        prediction = rf.predict(input_df)[0]
        proba = rf.predict_proba(input_df)[0][1]
        st.success(f"Prediction: {'Canceled' if prediction == 1 else 'Not Canceled'}")
        st.info(f"Probability of cancellation: {proba:.2f}")
