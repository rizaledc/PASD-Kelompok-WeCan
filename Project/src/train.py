# src/train.py
import sys
import os
# Tambahkan direktori root proyek ke sys.path agar modul 'src' dapat diimpor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import load_data
from src.feature_engineering import add_features
from src.preprocessing import DataProcessor
from src.model import Predictor
from sklearn.model_selection import train_test_split, GridSearchCV
import pickle
import numpy as np

def main():
    # Muat data training
    train_data_path = 'data/train_dataset.csv'
    df_train = load_data(train_data_path)
    if df_train is None:
        return

    # Lakukan rekayasa fitur (jika diperlukan)
    df_train = add_features(df_train)

    # Inisialisasi DataProcessor dan proses data
    processor = DataProcessor()
    df_train = processor.clean_data(df_train)
    df_train = processor.encode_target(df_train, 'lulus')
    feature_cols = ['nilai_ujian', 'kehadiran', 'partisipasi', 'rata_rata']
    df_train = processor.normalize_data(df_train, feature_cols)

    # Pisahkan fitur dan target
    X = df_train[feature_cols].values
    y = df_train['lulus'].values

    # Bagi data menjadi training dan validasi (opsional)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- Hyperparameter Tuning dengan GridSearchCV ---
    from sklearn.linear_model import LogisticRegression
    param_grid = {
        'C': [0.01, 0.1, 1, 10, 100],
        'penalty': ['l2'],
        'solver': ['lbfgs']
    }
    # Lakukan GridSearchCV
    grid_search = GridSearchCV(LogisticRegression(), param_grid, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    print("Best Parameters:", grid_search.best_params_)
    print("Best CV Accuracy:", grid_search.best_score_)
    
    # Gunakan model dengan parameter terbaik
    predictor = Predictor()
    predictor.model = grid_search.best_estimator_

    # Evaluasi pada data validasi
    acc, report = predictor.evaluate(X_val, y_val)
    print(f"Validation Accuracy: {acc:.2f}")
    print("Validation Classification Report:")
    print(report)

    # Simpan model dan scaler ke file (opsional)
    with open('model.pkl', 'wb') as f:
        pickle.dump(predictor, f)
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(processor.scaler, f)

if __name__ == '__main__':
    main()