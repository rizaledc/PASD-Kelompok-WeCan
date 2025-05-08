from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Konfigurasi aplikasi
app.config['SECRET_KEY'] = 'fe970610e1010e493d1ac97d9cc31d6a9dba47a90ae9e6a1'  # Ganti dengan secret key yang lebih kuat
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://neondb_owner:npg_JiGIqv3O9hXs@ep-silent-cloud-a1ss36i2-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'  # Sesuaikan dengan kredensial database Anda
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True

# Inisialisasi objek SQLAlchemy
db = SQLAlchemy()

# Inisialisasi LoginManager
login_manager = LoginManager()

# Menghubungkan db dengan aplikasi Flask
db.init_app(app)

# Menghubungkan login_manager dengan aplikasi Flask
login_manager.init_app(app)
login_manager.login_view = 'login'

# Fungsi user_loader untuk memuat pengguna berdasarkan user_id
@login_manager.user_loader
def load_user(user_id):
    from app.models import User  # Mengimpor model User setelah aplikasi diinisialisasi
    return User.query.get(int(user_id))

# Mengimpor routes setelah aplikasi diinisialisasi untuk mencegah masalah circular import
from app import routes
