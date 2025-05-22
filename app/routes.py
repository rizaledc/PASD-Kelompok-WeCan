from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import User, PredictionHistory
from flask_login import login_user, login_required, current_user, logout_user
import re  # Untuk validasi password
import joblib  # Menggunakan joblib untuk memuat model
import numpy as np
import os

# Load model machine learning
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'ml_model', 'model.pkl')
model = joblib.load(MODEL_PATH)  # Memuat model untuk prediksi

# Kode Dosen Fix
VALID_DOSEN_CODE = 'DOSENTELYU'  # Kode dosen tetap (fix)

# Halaman utama (Dashboard)
@app.route('/')
@login_required
def home():
    if current_user.isStudent:
        # Kirim username ke template dashboard mahasiswa
        return render_template('dashboardmhs.html', username=current_user.username)
    else:
        # Untuk dashboard dosen, username sudah bisa diakses via current_user di template
        # 'result' akan dikirim oleh route 'predict' jika ada prediksi baru
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
            flash('Username atau password yang Anda masukkan salah.', 'danger')

    return render_template('login.html')

# Halaman register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']  # Mengambil nilai role (mahasiswa atau dosen)
        kode_dosen = request.form.get('kode_dosen', '').strip()  # Kode dosen jika memilih dosen

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

        # Validasi konfirmasi password
        if password != confirm_password:
            flash('Password dan konfirmasi password tidak cocok.', 'danger')
            return redirect(url_for('register'))

        # Set role dan kode dosen jika peran adalah dosen
        if role == 'dosen':
            if kode_dosen != VALID_DOSEN_CODE:  # Misalnya kode konfirmasi dosen adalah 'DOSENTELYU'
                flash('Kode konfirmasi dosen salah.', 'danger')
                return redirect(url_for('register'))
            isStudent = False  # Jika dosen, set isStudent menjadi False
        else:
            isStudent = True  # Jika mahasiswa, set isStudent menjadi True

        # Buat user baru
        user = User(username=username, isStudent=isStudent)
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
        # Ambil data dari form input
        nama = str(request.form['nama']).strip()  # Pastikan tidak ada spasi berlebih
        nim = int(request.form['nim'])

        # Validasi nilai yang dimasukkan
        nilai_ujian = float(request.form['nilai_ujian'].replace(',', '.'))
        kehadiran = float(request.form['kehadiran'].replace(',', '.'))
        keaktifan = float(request.form['keaktifan'].replace(',', '.'))

        # Validasi rentang nilai
        if not (1 <= nilai_ujian <= 100 and 1 <= kehadiran <= 100 and 1 <= keaktifan <= 100):
            flash('Silahkan masukkan angka/persentasi antara 1-100.', 'danger')
            return redirect(url_for('home'))

        # Prediksi dengan model
        features = np.array([[nilai_ujian, kehadiran, keaktifan]])
        prediction_raw = model.predict(features)[0]  # Menggunakan 0 atau 1
        result = "Lulus" if prediction_raw == 1 else "Tidak Lulus"

        # Simpan data prediksi ke database
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
        print(f'Error during prediction: {e}')  # Untuk debugging
        flash('Terjadi kesalahan saat melakukan prediksi. Pastikan semua input valid.', 'danger')
        return redirect(url_for('home'))

# Halaman Statistik
@app.route('/statistik')
@login_required
def statistik():
    # Ambil semua data prediksi
    all_predictions = PredictionHistory.query.all()

    # Hitung jumlah lulus dan tidak lulus dari semua data
    pass_count = sum([1 for p in all_predictions if p.result == 'Lulus'])
    fail_count = len(all_predictions) - pass_count

    # Hitung rata-rata nilai ujian dan persentase kelulusan dari semua data
    avg_score = 0
    pass_percentage = 0
    if all_predictions: # Pastikan all_predictions tidak kosong
        avg_score = sum([p.nilai_ujian for p in all_predictions]) / len(all_predictions)
        pass_percentage = (pass_count / len(all_predictions)) * 100

    # Render template statistik.html untuk semua pengguna
    # Kirim juga current_user agar template bisa menyesuaikan navigasi jika perlu (opsional)
    return render_template('statistik.html',
                           pass_count=pass_count,
                           fail_count=fail_count,
                           avg_score=avg_score,
                           pass_percentage=pass_percentage,
                           current_user_role='mahasiswa' if current_user.isStudent else 'dosen') # Opsional: untuk penyesuaian kecil di template jika ada


# Halaman Leaderboard
@app.route('/leaderboard')
@login_required
def leaderboard():
    try:
        # Mengambil semua prediksi dari seluruh pengguna
        # Menggunakan joinedload untuk efisiensi query jika User model sering diakses
        predictions = PredictionHistory.query.options(db.joinedload(PredictionHistory.user)).all()

        # Menyiapkan data mentah untuk leaderboard
        leaderboard_raw_data = []
        for prediction in predictions:
            # Pastikan objek user ada sebelum mengakses username
            nama = prediction.nama if prediction.nama else "N/A"
            leaderboard_raw_data.append({
                'nama': nama,  # Menampilkan nama yang diinputkan
                'nilai_ujian': prediction.nilai_ujian,
                'kehadiran': prediction.kehadiran,
                'keaktifan': prediction.keaktifan,
                'result': prediction.result
            })

        # Urutkan berdasarkan nilai ujian (dari tertinggi ke terendah)
        leaderboard_raw_data.sort(key=lambda x: x['nilai_ujian'], reverse=True)

        # Tambahkan ranking setelah diurutkan
        leaderboard_data_ranked = []
        for i, data_item in enumerate(leaderboard_raw_data):
            data_item['rank'] = i + 1  # Menambahkan key 'rank'. i untuk index, +1 untuk ranking mulai dari 1
            leaderboard_data_ranked.append(data_item)

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