# tests/test_feature_engineering.py
import unittest
import pandas as pd
from src.feature_engineering import add_features

class TestFeatureEngineering(unittest.TestCase):
    def setUp(self):
        # Buat dummy data
        self.df = pd.DataFrame({
            'kehadiran': [80, 60],
            'partisipasi': [90, 50]
        })

    def test_add_features(self):
        # Panggil fungsi add_features
        df_with_features = add_features(self.df)
        # Periksa apakah kolom 'kehadiran_partisipasi' sudah ada
        self.assertIn('kehadiran_partisipasi', df_with_features.columns)
        # Periksa apakah nilainya benar (perkalian kehadiran dan partisipasi)
        expected = self.df['kehadiran'] * self.df['partisipasi']
        pd.testing.assert_series_equal(df_with_features['kehadiran_partisipasi'], expected, check_names=False)

if __name__ == '__main__':
    unittest.main()
