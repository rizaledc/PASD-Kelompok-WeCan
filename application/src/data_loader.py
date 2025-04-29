# src/data_loader.py
import pandas as pd

def load_data(file_path):
    """
    Memuat dataset dari file CSV dan mengembalikan DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error saat memuat data: {e}")
        return None