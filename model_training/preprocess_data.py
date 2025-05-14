import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_data(file_path):
    """Memuat data dari file CSV."""
    data = pd.read_csv(file_path)
    return data

def preprocess_data(data):
    """Melakukan preprocessing pada data: membersihkan dan menormalkan data."""
    # Menghapus data yang hilang
    data = data.dropna()
    
    # Mengubah kolom 'Kelulusan' menjadi numerik (0 = Tidak Lulus, 1 = Lulus)
    data['Kelulusan'] = data['Kelulusan'].apply(lambda x: 1 if x == 'Lulus' else 0)
    
    # Memisahkan fitur dan label
    X = data[['Nilai Ujian', 'Kehadiran', 'Keaktifan']]
    y = data['Kelulusan']
    
    # Normalisasi fitur menggunakan StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    

    return X_scaled, y
