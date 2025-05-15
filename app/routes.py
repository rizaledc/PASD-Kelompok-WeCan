from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import User, PredictionHistory
from flask_login import login_user, login_required, current_user, logout_user
import re  # Untuk validasi password
import joblib  # or use 'import pickle' if you used pickle
import numpy as np
import os
import sklearn

##Call model.pkl for predict##
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'ml_model', 'model.pkl')
model = joblib.load(MODEL_PATH)# Load your model here

# Halaman utama (dashboard)
@app.route('/')
@login_required
def home():
    return render_template('dashboard.html')

# Halaman login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            if not user:
                flash('Username yang Anda masukkan salah.', 'danger')
            else:
                flash('Password yang Anda masukkan salah.', 'danger')

    return render_template('login.html')

# Halaman register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validasi username: minimal 8 karakter dan unik
        if len(username) < 8:
            flash('Username harus terdiri dari minimal 8 karakter.', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('Username sudah digunakan.', 'danger')
            return redirect(url_for('register'))

        # Validasi password: minimal 8 karakter dan mengandung angka dan huruf
        if len(password) < 8 or not re.search(r"\d", password) or not re.search(r"[a-zA-Z]", password):
            flash('Password harus terdiri dari minimal 8 karakter, dan mengandung angka dan huruf.', 'danger')
            return redirect(url_for('register'))

        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('Akun Anda telah dibuat!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Halaman logout
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Anda telah berhasil logout', 'info')
    return redirect(url_for('login'))  # Arahkan ke halaman login setelah logout

# Halaman prediksi
@app.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        ## FOR DATABASE INPUT ##
        nama = str(request.form['nama'])
        nim = int(request.form['nim'])

        ## FOR MODEL PREDICTION ##
        nilai_ujian = float(request.form['nilai_ujian'].replace(',', '.'))
        kehadiran = float(request.form['kehadiran'].replace(',', '.'))
        keaktifan = float(request.form['keaktifan'].replace(',', '.'))

        # Check value ranges
        if not (1 <= nilai_ujian <= 100 and 1 <= kehadiran <= 100 and 1 <= keaktifan <= 100):
            flash('Silahkan masukan angka/persentasi 1-100', 'danger')
            return redirect(url_for('home'))

        ### 🔍 Call the machine learning model ###
        features = np.array([[nilai_ujian, kehadiran, keaktifan]])
        prediction_raw = model.predict(features)[0]  # returns 0 or 1
        result = "Lulus" if prediction_raw == 1 else "Tidak Lulus"

        ### 🧾 Save to database ###
        prediction = PredictionHistory(
            user_id=current_user.id,
            nama=nama,
            nim=nim,
            nilai_ujian=nilai_ujian,
            kehadiran=kehadiran,
            keaktifan=keaktifan,
            result=result
        )
        db.session.add(prediction)
        db.session.commit()

        flash(f'Prediksi Anda: {result}', 'success')
        return render_template('dashboard.html', result=result)

    except Exception as e:
        print(f'Error during prediction: {e}')  # For debugging
        flash('Terjadi kesalahan saat melakukan prediksi.', 'danger')
        return redirect(url_for('home'))


# Halaman Statistik
@app.route('/statistik')
@login_required
def statistik():
    # Mengambil semua prediksi dari seluruh pengguna
    predictions = PredictionHistory.query.all()

    # Menghitung jumlah lulus dan tidak lulus
    pass_count = sum([1 for p in predictions if p.result == 'Lulus'])
    fail_count = len(predictions) - pass_count  # Total - pass_count

    # Menghitung rata-rata nilai ujian dan persentase kelulusan
    avg_score = sum([p.nilai_ujian for p in predictions]) / len(predictions) if predictions else 0
    pass_percentage = (pass_count / len(predictions)) * 100 if predictions else 0

    # Menghitung prediksi per pengguna
    pass_pred = [p.result for p in predictions if p.result == 'Lulus']
    fail_pred = [p.result for p in predictions if p.result == 'Tidak Lulus']

    # Membuat data untuk chart (misalnya untuk total lulus dan tidak lulus)
    return render_template('statistik.html', 
                        avg_score=avg_score, 
                        pass_percentage=pass_percentage,
                        pass_count=pass_count, 
                        fail_count=fail_count,
                        total_predictions=len(predictions),
                        pass_pred=pass_pred, 
                        fail_pred=fail_pred)


# Halaman Leaderboard
@app.route('/leaderboard')
@login_required
def leaderboard():
    try:
        # Mengambil top 10 prediksi dengan status "Lulus" dan nilai ujian tertinggi
        top_lulus_predictions = PredictionHistory.query \
            .options(db.joinedload(PredictionHistory.user)) \
            .filter(PredictionHistory.result == "Lulus") \
            .order_by(PredictionHistory.nilai_ujian.desc()) \
            .limit(10) \
            .all()

        leaderboard_data_ranked = []
        for i, prediction in enumerate(top_lulus_predictions): 
            # Pastikan objek user ada sebelum mengakses username
            username = prediction.user.username if prediction.user else "N/A"
            leaderboard_data_ranked.append({
                'rank': i + 1,  # Ranking berdasarkan urutan dari query
                'username': username,
                'nilai_ujian': prediction.nilai_ujian,
                'kehadiran': prediction.kehadiran,
                'keaktifan': prediction.keaktifan,
                'result': prediction.result  # Ini akan selalu "Lulus" berdasarkan filter
            })

        return render_template('leaderboard.html', leaderboard_data=leaderboard_data_ranked)

    except AttributeError as e:
        app.logger.error(f"Leaderboard AttributeError: {e}") # Untuk debugging di log server
        flash('Terjadi kesalahan saat mengambil data pengguna untuk leaderboard.', 'danger')
        return render_template('leaderboard.html', leaderboard_data=[], error_message="Kesalahan data pengguna.")
    except Exception as e:
        app.logger.error(f"Leaderboard general error: {e}") # Untuk debugging di log server
        flash('Terjadi kesalahan saat memuat leaderboard.', 'danger')
        return render_template('leaderboard.html', leaderboard_data=[], error_message="Kesalahan server.")

# Halaman Profil
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', username=current_user.username)