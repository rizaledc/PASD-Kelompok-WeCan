from flask import render_template, request
from app import app
import joblib
import pandas as pd

# Memuat model yang sudah disimpan
model = joblib.load('app/ml_model/model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Mendapatkan data input dari form dan mengonversi menjadi float
        nilai_ujian = float(request.form['nilai_ujian'])
        kehadiran = float(request.form['kehadiran'])
        keaktifan = float(request.form['keaktifan'])
        
        # Validasi input: pastikan nilai berada antara 0 dan 100
        if not (0 <= nilai_ujian <= 100):
            return render_template('index.html', result="Nilai Ujian harus antara 0 dan 100.")
        
        if not (0 <= kehadiran <= 100):
            return render_template('index.html', result="Kehadiran harus antara 0 dan 100.")
        
        if not (0 <= keaktifan <= 100):
            return render_template('index.html', result="Keaktifan harus antara 0 dan 100.")
        
        # Menyusun data input
        input_data = pd.DataFrame([[nilai_ujian, kehadiran, keaktifan]], columns=['Nilai Ujian', 'Kehadiran', 'Keaktifan'])

        # Melakukan prediksi
        prediksi = model.predict(input_data)
        status_kelulusan = 'Lulus' if prediksi[0] == 1 else 'Tidak Lulus'
        
        return render_template('index.html', result=status_kelulusan)
    
    except Exception as e:
        return str(e)