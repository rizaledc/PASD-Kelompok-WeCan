# tests/test_data_loader.py
import unittest
from src.data_loader import load_data

class TestDataLoader(unittest.TestCase):
    def test_load_data(self):
        df = load_data('data/train_dataset.csv')
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)

if __name__ == '__main__':
    unittest.main()
