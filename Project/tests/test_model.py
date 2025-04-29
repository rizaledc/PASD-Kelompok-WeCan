# tests/test_model.py
import unittest
import numpy as np
from src.model import Predictor

class TestModel(unittest.TestCase):
    def setUp(self):
        # Buat dummy data untuk training dan testing
        self.X_train = np.array([[1, 2, 3, 4],
                                 [2, 3, 4, 5],
                                 [3, 4, 5, 6],
                                 [4, 5, 6, 7]])
        self.y_train = np.array([1, 0, 1, 0])
        self.X_test = np.array([[1, 2, 3, 4],
                                [4, 5, 6, 7]])
        # Target dummy untuk evaluasi test
        self.y_test = np.array([1, 0])
    
    def test_train_and_predict(self):
        predictor = Predictor()
        predictor.train_model(self.X_train, self.y_train)
        y_pred = predictor.predict(self.X_test)
        # Periksa jumlah prediksi harus sama dengan jumlah data test
        self.assertEqual(len(y_pred), len(self.X_test))
        # Periksa bahwa prediksi hanya menghasilkan 0 atau 1
        self.assertTrue(np.all(np.isin(y_pred, [0, 1])))
    
    def test_evaluate(self):
        predictor = Predictor()
        predictor.train_model(self.X_train, self.y_train)
        acc, report = predictor.evaluate(self.X_test, self.y_test)
        self.assertIsInstance(acc, float)
        # Laporan klasifikasi harus berupa string dan mengandung informasi metrik
        self.assertIsInstance(report, str)
        self.assertIn("precision", report.lower())

if __name__ == '__main__':
    unittest.main()
