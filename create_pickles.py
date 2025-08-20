# create_pickles.py
import os
import pickle

# --- Pastikan folder models ada ---
os.makedirs("models", exist_ok=True)

# --- Semua kolom fitur pipeline ---
training_columns = [
    "hotel",
    "lead_time",
    "arrival_date_year",
    "arrival_date_month",
    "arrival_date_week_number",
    "arrival_date_day_of_month",
    "stays_in_weekend_nights",
    "stays_in_week_nights",
    "adults",
    "children",
    "babies",
    "meal",
    "country",
    "market_segment",
    "distribution_channel",
    "is_repeated_guest",
    "previous_cancellations",
    "previous_bookings_not_canceled",
    "reserved_room_type",
    "assigned_room_type",
    "booking_changes",
    "deposit_type",
    "days_in_waiting_list",
    "customer_type",
    "adr",
    "required_car_parking_spaces",
    "total_of_special_requests",
    "has_agent"
]

# --- Kolom kategorikal saja ---
categorical_cols = [
    "hotel",
    "arrival_date_month",
    "meal",
    "country",
    "market_segment",
    "distribution_channel",
    "reserved_room_type",
    "assigned_room_type",
    "deposit_type",
    "customer_type",
    "required_car_parking_spaces",
    "has_agent"
]

# --- Simpan pickle ---
with open("models/training_columns.pkl", "wb") as f:
    pickle.dump(training_columns, f)

with open("models/categorical_cols.pkl", "wb") as f:
    pickle.dump(categorical_cols, f)

print("✅ training_columns.pkl & categorical_cols.pkl berhasil dibuat di folder models/")
