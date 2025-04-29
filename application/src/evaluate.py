# src/evaluate.py
import sys
import os
# Tambahkan direktori root proyek ke sys.path agar modul 'src' dapat diimpor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import load_data
from src.feature_engineering import add_features
import pickle
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report

def evaluate():
    # Muat data testing
    test_data_path = 'data/test_dataset.csv'
    df_test = load_data(test_data_path)
    if df_test is None:
        return

    # Rekayasa fitur (jika diperlukan)
    df_test = add_features(df_test)

    # Proses pra-pemrosesan manual agar dapat menggunakan scaler yang disimpan
    feature_cols = ['nilai_ujian', 'kehadiran', 'partisipasi', 'rata_rata']
    df_test = df_test.dropna().copy()
    
    # Tentukan target_col secara terpisah
    target_col = 'lulus'
    df_test[target_col] = df_test[target_col].apply(lambda x: 1 if x.strip().lower() == 'ya' else 0)

    X_test = df_test[feature_cols].values
    y_test = df_test[target_col].values

    # Muat scaler yang telah disimpan
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    X_test_scaled = scaler.transform(pd.DataFrame(X_test,columns=feature_cols))

    # Muat model yang telah disimpan
    with open('model.pkl', 'rb') as f:
        predictor = pickle.load(f)

    # Prediksi dan evaluasi
    y_pred = predictor.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, zero_division=0)

    print("Test Accuracy: {:.2f}".format(acc))
    print("Test Classification Report:")
    print(report)

if __name__ == '__main__':
    evaluate()