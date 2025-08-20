# train_model_20pct.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("data/cleaned_hotel_data4.csv")  # ganti sesuai path dataset

# -----------------------------
# Sampling 20% data
# -----------------------------
df_sample = df.sample(frac=0.2, random_state=42)  # 20% dari total data

# -----------------------------
# Tentukan fitur dan target
# -----------------------------
target = "is_canceled"
features = [col for col in df_sample.columns if col != target]

X = df_sample[features]
y = df_sample[target]

# -----------------------------
# One-Hot Encoding untuk fitur kategorikal
# -----------------------------
X = pd.get_dummies(X)

# Simpan nama kolom training (untuk prediksi nanti)
training_columns = X.columns.tolist()
joblib.dump(training_columns, "models/training_columns_20pct.pkl")

# -----------------------------
# Split data untuk validasi (opsional)
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# Latih Random Forest
# -----------------------------
rf = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)
rf.fit(X_train, y_train)

# -----------------------------
# Simpan model
# -----------------------------
joblib.dump(rf, "models/rf_model_20pct.pkl")

print("✅ Model dan training columns berhasil disimpan!")
