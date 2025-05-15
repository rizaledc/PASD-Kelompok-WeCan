from app import db  # Mengimpor db yang sudah diinisialisasi di __init__.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Model Pengguna
class User(UserMixin, db.Model):
    __tablename__ = 'user_tb'  # Nama tabel yang digunakan di database

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    isStudent = db.Column(db.Boolean, default=True)  # True untuk mahasiswa, False untuk dosen
    kode_dosen = db.Column(db.String(255), nullable=True)  # Kolom untuk kode dosen, hanya untuk dosen

    def set_password(self, password):
        """Mengenkripsi password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Memverifikasi password."""
        return check_password_hash(self.password, password)

# Model Riwayat Prediksi (PredictionHistory)
class PredictionHistory(db.Model):
    __tablename__ = 'prediction_history'  # Nama tabel yang akan digunakan di database

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_tb.id'), nullable=False)  # Relasi ke tabel User
    nama = db.Column(db.String(255), nullable=False)
    nim = db.Column(db.Integer, nullable=False)
    nilai_ujian = db.Column(db.Float, nullable=False)
    kehadiran = db.Column(db.Float, nullable=False)
    keaktifan = db.Column(db.Float, nullable=False)
    result = db.Column(db.String(100), nullable=False)

    user = db.relationship('User', backref='predictions', lazy=True)  # Relasi balik ke model User
