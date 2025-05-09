from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Konfigurasi aplikasi
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

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
