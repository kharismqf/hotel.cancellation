import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load data
df = pd.read_csv("data/cleaned_hotel_data.csv")

# Ambil 20% sample
df_sample = df.sample(frac=0.2, random_state=42)

# Tentukan X dan y
X = df_sample.drop(columns=["is_canceled"])
y = df_sample["is_canceled"]

# Preprocessing OHE (contoh sederhana)
X = pd.get_dummies(X)
training_columns = X.columns

# Train model
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X, y)

# Simpan model & training columns
joblib.dump(rf, "models/rf_model_20pct.pkl")
joblib.dump(list(training_columns), "models/training_columns_20pct.pkl")
