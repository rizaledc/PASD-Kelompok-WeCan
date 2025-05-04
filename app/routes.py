from flask import render_template, request, jsonify
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
        # Mendapatkan data input dari form
        nilai_ujian = float(request.form['nilai_ujian'])
        kehadiran = float(request.form['kehadiran'])
        keaktifan = float(request.form['keaktifan'])
        
        # Menyusun data input
        input_data = pd.DataFrame([[nilai_ujian, kehadiran, keaktifan]], columns=['Nilai Ujian', 'Kehadiran', 'Keaktifan'])

        # Melakukan prediksi
        prediksi = model.predict(input_data)
        status_kelulusan = 'Lulus' if prediksi[0] == 1 else 'Tidak Lulus'
        
        return render_template('index.html', result=status_kelulusan)
    
    except Exception as e:
        return str(e)
