import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load cleaned data
df = pd.read_csv("data/cleaned_hotel_data.csv")  # sesuaikan path

# Pilih target dan fitur
X = df.drop(columns=["is_canceled"])
y = df["is_canceled"]

# Sampling 20% dari total data
X_sample, _, y_sample, _ = train_test_split(X, y, test_size=0.8, random_state=42, stratify=y)

# Buat Random Forest ringan
rf = RandomForestClassifier(
    n_estimators=150,
    max_depth=10,
    random_state=42
)

# Train model
rf.fit(X_sample, y_sample)

# Simpan model dan training columns
joblib.dump(rf, "models/rf_model.pkl", compress=3)
joblib.dump(list(X.columns), "models/training_columns.pkl", compress=3)

print("Training selesai, model dan training_columns.pkl telah tersimpan!")
