# tests/test_train.py
import unittest
import os
import pandas as pd
import tempfile
from src.train import main as train_main

class TestTrain(unittest.TestCase):
    def setUp(self):
        # Buat direktori temporary untuk file dummy
        self.temp_dir = tempfile.TemporaryDirectory()
        self.train_file_path = os.path.join(self.temp_dir.name, "train_dataset.csv")
        
        # Buat dummy dataset dengan minimal 10 baris data
        df = pd.DataFrame({
            'nilai_ujian': [80, 45, 60, 30, 70, 55, 65, 75, 50, 85],
            'kehadiran': [90, 50, 70, 40, 80, 60, 75, 85, 55, 95],
            'partisipasi': [85, 40, 75, 35, 65, 45, 80, 90, 50, 88],
            'rata_rata': [85, 45, 68, 35, 71, 53, 73, 83, 52, 89],
            'lulus': ['Ya', 'Tidak', 'Ya', 'Tidak', 'Ya', 'Tidak', 'Ya', 'Ya', 'Tidak', 'Ya']
        })
        df.to_csv(self.train_file_path, index=False)
        
        # Simpan file dummy ke folder data/
        self.original_train_path = "data/train_dataset.csv"
        os.makedirs("data", exist_ok=True)
        if os.path.exists(self.original_train_path):
            self.backup_train = self.original_train_path + ".bak"
            os.rename(self.original_train_path, self.backup_train)
        os.replace(self.train_file_path, self.original_train_path)

    def tearDown(self):
        # Hapus file dummy dan kembalikan backup jika ada
        if os.path.exists(self.original_train_path):
            os.remove(self.original_train_path)
        if hasattr(self, 'backup_train') and os.path.exists(self.backup_train):
            os.rename(self.backup_train, self.original_train_path)
        self.temp_dir.cleanup()

    def test_train_main(self):
        # Uji bahwa fungsi main() dari train.py berjalan tanpa error
        try:
            train_main()
        except Exception as e:
            self.fail(f"train.main() menimbulkan exception: {e}")

if __name__ == '__main__':
    unittest.main()
