from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def evaluate_model(model, X_test, y_test):
    """Mengevaluasi model menggunakan berbagai metrik."""
    # Memprediksi hasil dengan data uji
    y_pred = model.predict(X_test)
    
    # Menghitung metrik evaluasi
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    # Menampilkan hasil evaluasi
    print(f"Akurasi: {accuracy * 100:.2f}%")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")

    print(f"F1 Score: {f1:.2f}")
    # Mengembalikan hasil evaluasi dalam bentuk dictionary
