from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import User, PredictionHistory
from flask_login import login_user, login_required, current_user, logout_user


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
            flash('Username atau password salah.', 'danger')

    return render_template('login.html')


# Halaman register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Cek jika username sudah ada
        if User.query.filter_by(username=username).first():
            flash('Username sudah digunakan.', 'danger')
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
