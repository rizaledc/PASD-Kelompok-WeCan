import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Memuat data
data = pd.read_csv('app/data/data_kelulusan_mahasiswa.csv')

# Memisahkan fitur dan label
X = data[['Nilai Ujian', 'Kehadiran', 'Keaktifan']]
y = data['Kelulusan'].apply(lambda x: 1 if x == 'Lulus' else 0)  # Mengubah 'Lulus' dan 'Tidak Lulus' menjadi 1 dan 0

# Pembagian data menjadi training dan testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Membuat model RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Melatih model
model.fit(X_train, y_train)

# Memprediksi data uji
y_pred = model.predict(X_test)

# Menilai akurasi model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Menyimpan model
joblib.dump(model, 'app/ml_model/model.pkl')