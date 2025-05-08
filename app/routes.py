from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import User, PredictionHistory
from flask_login import login_user, login_required, current_user, logout_user

# Halaman utama (hanya bisa diakses setelah login)
@app.route('/')
def home():
    if current_user.is_authenticated:  # Memeriksa apakah pengguna sudah login
        return render_template('dashboard.html') 
    else:
        return redirect(url_for('login'))  # Jika belum login, arahkan ke halaman login

# Halaman login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # Jika pengguna sudah login
        return redirect(url_for('home'))  # Arahkan ke halaman utama
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Cek apakah pengguna ada di database
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):  # Verifikasi password
            login_user(user)
            return redirect(url_for('home'))  # Arahkan ke halaman utama setelah login
        else:
            flash('Username atau password salah.', 'danger')
    return render_template('login.html')  # Kembali ke halaman login jika gagal login

# Halaman register
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Jika pengguna sudah login, arahkan ke halaman utama
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Membuat pengguna baru
        user = User(username=username)
        user.set_password(password)  # Set password yang terenkripsi

        db.session.add(user)
        db.session.commit()

        flash('Akun Anda telah dibuat!', 'success')
        return redirect(url_for('login'))  # Setelah registrasi berhasil, arahkan ke halaman login

    return render_template('register.html')

# Halaman logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah berhasil logout', 'info')
    return redirect(url_for('login'))  # Arahkan ke halaman login setelah logout

# Halaman prediksi
@app.route('/predict', methods=['POST'])
@login_required  # Pastikan hanya pengguna yang login yang bisa melakukan prediksi
def predict():
    try:
        nilai_ujian = float(request.form['nilai_ujian'])
        kehadiran = float(request.form['kehadiran'])
        keaktifan = float(request.form['keaktifan'])

        # Prediksi (misalnya: jika nilai ujian > 60, maka lulus, jika tidak tidak lulus)
        result = "Lulus" if nilai_ujian >= 60 else "Tidak Lulus"

        # Menyimpan riwayat prediksi
        prediction = PredictionHistory(
            user_id=current_user.id,
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
        flash('Terjadi kesalahan saat melakukan prediksi.', 'danger')
        return redirect(url_for('home'))
