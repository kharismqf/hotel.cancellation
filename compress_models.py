import joblib
from pathlib import Path

# Folder models
models_path = Path("models")

# Compress semua .pkl di folder models dan overwrite
for pkl_file in models_path.glob("*.pkl"):
    print(f"Compressing {pkl_file.name}...")
    
    # Load model / object
    obj = joblib.load(pkl_file)
    
    # Simpan lagi dengan compress level 3, overwrite
    joblib.dump(obj, pkl_file, compress=3)
    
    print(f"{pkl_file.name} compressed and overwritten successfully!")
