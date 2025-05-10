# Aplikasi Pendeteksi Kelulusan
Proyek ini adalah bagian dari mata kuliah PASD yang dikembangkan oleh Kelompok WeCan. Repositori ini berisi kode sumber untuk sistem informasi yang mencakup modul-modul penting seperti Portofolio dan Leaderboard.

## Daftar Isi
- [Fitur Utama](#fitur-utama)
- [Konsep Penting](#konsep-penting)
- [Instalasi & Setup](#instalasi--setup)
- [Cara Menjalankan Aplikasi](#cara-menjalankan-aplikasi)
- [Alur Kerja Git (Pull & Push)](#alur-kerja-git-pull--push)
- [Status Proyek & To-Do List](#status-proyek--to-do-list)
- [Kontributor](#kontributor)

## Fitur Utama

### Modul Portofolio
Modul ini menangani data portofolio pengguna dalam sistem.
- *Register & Register Educator:* Mekanisme pendaftaran untuk pengguna biasa dan edukator.
- *Roll Verification:* Proses verifikasi peran pengguna (memerlukan 2 file HTML terpisah untuk implementasi UI/UX).

### Modul Leaderboard
Modul ini menampilkan peringkat dan statistik pengguna.
- *Leaderboard Mahasiswa:* Mahasiswa hanya dapat melihat tampilan leaderboard.
- *Leaderboard Dosen:* Dosen memiliki hak akses untuk menginput data dan melihat visualisasi statistik dari leaderboard.
- *Requirement Data:* Sistem dirancang untuk menangani templat minimal 50 input data per sesi (siding data).
- *Balance Calculation:* Menghitung statistik 'balance' (misalnya, nilai tertinggi) dari data yang diinput.
- *Aksesibilitas:* Leaderboard dapat diakses oleh kedua peran (Mahasiswa dan Dosen) meskipun dengan fungsi yang berbeda.

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

## Alur Kerja Git (Pull & Push)

Berikut adalah panduan singkat untuk alur kerja Git dalam tim:

### Mendapatkan Kode Terbaru dari main

Sebelum memulai pekerjaan baru, selalu pastikan Anda memiliki kode terbaru dari branch main:

1.  Masuk ke direktori proyek:
    bash
    cd PASD-Kelompok-WeCan
    
2.  Pindah ke branch main:
    bash
    git checkout main
    
3.  Ambil perubahan terbaru dari GitHub:
    bash
    git pull origin main
    

### Membuat Branch Baru untuk Fitur/Perbaikan

Kerjakan fitur atau perbaikan bug di branch terpisah untuk menghindari konflik.
Ada dua cara umum:

1.  *Via VS Code Command Palette:*
    *   Tekan Ctrl+Shift+P (atau Cmd+Shift+P di VSCode).
    *   Ketik Git: Create Branch.
    *   Masukkan nama branch baru, misalnya feature/leaderboard-viz atau bugfix/login-error. (Disarankan menggunakan nama yang deskriptif).
2.  *Via Command Line:*
    bash
    git checkout -b nama-branch-anda
    # Contoh: git checkout -b feature/add-educator-reg
    # Contoh: git checkout -b bugfix/fix-leaderboard-balance
    
    Setelah membuat branch baru, pastikan Anda sudah beralih ke branch tersebut (gunakan git status untuk memeriksa).

### Mendorong (Push) Perubahan Anda

Setelah selesai mengerjakan fitur/perbaikan di branch Anda:

1.  Periksa file yang diubah (optional tapi disarankan):
    bash
    git status
    
2.  Tambahkan (stage) semua perubahan yang ingin di-commit:
    bash
    git add .
    # Atau tambahkan file spesifik: git add path/to/your/file.html
    
3.  Commit perubahan dengan pesan yang jelas:
    bash
    git commit -m "Pesan commit Anda yang menjelaskan perubahan"
    
4.  Dorong (push) branch lokal Anda ke GitHub:
    bash
    git push origin nama-branch-anda
    # Ganti 'nama-branch-anda' dengan nama branch yang baru saja Anda buat
    # Contoh: git push origin feature/add-educator-reg
    
5.  *Buat Pull Request (PR) di GitHub:*
    *   Buka repositori proyek di browser (GitHub).
    *   Biasanya akan muncul banner yang menawarkan untuk membuat Pull Request dari branch yang baru saja di-push. Jika tidak, masuk ke tab "Pull requests" dan klik "New pull request".
    *   Pilih branch Anda sebagai compare dan main sebagai base.
    *   Tambahkan judul dan deskripsi PR yang jelas tentang apa yang Anda kerjakan.
    *   Request review dari anggota tim lain jika diperlukan.

## Status Proyek & To-Do List

Berikut adalah daftar tugas yang sedang atau akan dikerjakan:

- [ ] Menyelesaikan implementasi penuh Modul Portofolio (Registrasi, Registrasi Educator, Roll Verification).
- [ ] Mengembangkan logika backend untuk Modul Leaderboard (Input data Dosen, perhitungan balance).
- [ ] Membuat tampilan visualisasi statistik Leaderboard untuk peran Dosen.
- [ ] Memastikan sistem dapat menangani minimal 50 input data untuk leaderboard.
- [ ] Merapikan dan meningkatkan UI/UX pada halaman-halaman yang sudah ada.
- [ ] Menulis dokumentasi lebih lanjut untuk setiap modul.
- [ ] Melakukan testing pada setiap fitur.
- [ ] [Tambahkan item to-do lain di sini]

## Kontributor

Proyek ini dikembangkan oleh Kelompok WeCan:
- Admin 
- [Rizal Wahyu Pratama] - [Fitur registrasi]
- [Khulika Malkan] - [Peran/Kontribusi]
- [Mikhael Setia Budi] - [Peran/Kontribusi]
- [Irena Cahya Resinah] - [Peran/Kontribusi]
---