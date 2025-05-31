# Tel-UGrad: Telkom University Graduate Predictor
Proyek ini adalah bagian dari mata kuliah PASD yang dikembangkan oleh Kelompok WeCan. Repositori ini berisi kode sumber untuk sistem informasi yang mencakup modul-modul penting serta alur kerja aplikasinya.

## Daftar Isi
- [Konsep Penting](#konsep-penting)
- [Instalasi & Setup](#instalasi--setup)
- [Cara Menjalankan Aplikasi](#cara-menjalankan-aplikasi)
- [Kontributor](#kontributor)

## Konsep Penting
- *Inheritance:* Digunakan terutama pada *Model Data* untuk struktur yang jelas dan terorganisir. Fungsionalitas utama (logika bisnis) ditangani di bagian lain dari kode (misalnya, di controller/service layer).

## Instalasi & Setup
Untuk menjalankan proyek ini di lingkungan lokal Anda, ikuti langkah-langkah berikut:
1.  *Clone Repositori:*
    bash
    git clone https://github.com/rizaledc/PASD-Kelompok-WeCan.git
    
2.  *Masuk ke Direktori Proyek:*
    bash
    cd Nama-Folder-Proyek-Anda
    
3.  *Buat dan Aktifkan Virtual Environment (venv):*
    *   *Windows:*
        bash
        python -m venv venv
        .\venv\Scripts\activate
        
4.  *Instal Dependensi:*
    Pastikan Anda memiliki file requirements.txt di root proyek yang berisi daftar library yang dibutuhkan (misalnya Flask).
    bash
    pip install -r requirements.txt
    
    *(Jika file requirements.txt belum ada, buatlah dengan pip freeze > requirements.txt setelah menginstal semua library yang dibutuhkan secara manual).*

## Cara Menjalankan Aplikasi
Setelah setup selesai dan virtual environment aktif, jalankan aplikasi Flask:
1.  Pastikan Anda berada di root folder proyek dan venv sudah aktif.
2.  Jalankan perintah:
    bash
    flask run
3.  Aplikasi akan berjalan di http://127.0.0.1:5000/ (atau alamat lain yang tertera di output terminal).


## Kontributor
Proyek ini dikembangkan oleh Kelompok WeCan:
- [Rizal Wahyu Pratama] - [Fitur login, registrasi, profile]
- [Khulika Malkan] - [Fitur dashboard, Statistika dan Leaderboard]
- [Mikhael Setia Budi] - [Membuat dan Mengintegrasikan Dashboard]
- [Irena Cahya Resinah] - [Merapihkan UI (tampilan Aplikasi)]
---