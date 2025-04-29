# tests/test_preprocessing.py
import unittest
import pandas as pd
from src.preprocessing import DataProcessor

class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        data = {
            'nilai_ujian': [80, 45],
            'kehadiran': [90, 50],
            'partisipasi': [85, 40],
            'rata_rata': [85, 45],
            'lulus': ['Ya', 'Tidak']
        }
        self.df = pd.DataFrame(data)
        self.processor = DataProcessor()

    def test_clean_data(self):
        df_clean = self.processor.clean_data(self.df)
        self.assertEqual(len(df_clean), len(self.df))

    def test_encode_target(self):
        df_encoded = self.processor.encode_target(self.df.copy(), 'lulus')
        self.assertTrue(df_encoded['lulus'].isin([0, 1]).all())

if __name__ == '__main__':
    unittest.main()