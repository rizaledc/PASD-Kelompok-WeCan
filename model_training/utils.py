import joblib

def save_model(model, filename):
    """Menyimpan model ke file menggunakan joblib."""
    joblib.dump(model, filename)
    print(f"Model telah disimpan di {filename}")

def load_model(filename):
    """Memuat model dari file menggunakan joblib."""
    model = joblib.load(filename)
    print(f"Model telah dimuat dari {filename}")
    return model