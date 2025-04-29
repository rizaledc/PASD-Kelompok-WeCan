# src/preprocessing.py
import pandas as pd
from sklearn.preprocessing import StandardScaler

class DataProcessor:
    """
    Kelas untuk memproses data sebelum digunakan oleh model.
    """
    def __init__(self):
        self.scaler = None

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Membersihkan data: menghapus baris yang memiliki nilai NaN.
        """
        df_clean = df.dropna().copy()
        return df_clean

    def encode_target(self, df: pd.DataFrame, target_col: str) -> pd.DataFrame:
        """
        Mengonversi kolom target (Ya/Tidak) menjadi 1/0.
        """
        df[target_col] = df[target_col].apply(lambda x: 1 if x.strip().lower() == 'ya' else 0)
        return df

    def normalize_data(self, df: pd.DataFrame, feature_cols: list) -> pd.DataFrame:
        """
        Melakukan normalisasi pada kolom fitur.
        """
        if self.scaler is None:
            self.scaler = StandardScaler()
            df[feature_cols] = self.scaler.fit_transform(df[feature_cols])
        else:
            df[feature_cols] = self.scaler.transform(df[feature_cols])
        return df
