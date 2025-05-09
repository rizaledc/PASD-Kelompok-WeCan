from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import User, PredictionHistory
from flask_login import login_user, login_required, current_user, logout_user
import re  # Untuk validasi password

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
        nilai_ujian = float(request.form['nilai_ujian'])
        kehadiran = float(request.form['kehadiran'])
        keaktifan = float(request.form['keaktifan'])

        if not (1 <= nilai_ujian <= 100 and 1 <= kehadiran <= 100 and 1 <= keaktifan <= 100):
            flash('Silahkan masukan angka/persentasi 1-100', 'danger')
            return redirect(url_for('home'))

        result = "Lulus" if nilai_ujian >= 60 else "Tidak Lulus"

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

# Halaman Statistik
@app.route('/statistik')
@login_required
def statistik():
    predictions = PredictionHistory.query.filter_by(user_id=current_user.id).all()

    # Menghitung jumlah lulus dan tidak lulus
    pass_count = sum([1 for p in predictions if p.result == 'Lulus'])
    fail_count = len(predictions) - pass_count  # Total - pass_count

    # Menghitung rata-rata nilai ujian dan persentase kelulusan
    avg_score = sum([p.nilai_ujian for p in predictions]) / len(predictions) if predictions else 0
    pass_percentage = (pass_count / len(predictions)) * 100 if predictions else 0

    return render_template('statistik.html', 
                           avg_score=avg_score, 
                           pass_percentage=pass_percentage,
                           pass_count=pass_count, 
                           fail_count=fail_count)

# Halaman Profil
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', username=current_user.username)
