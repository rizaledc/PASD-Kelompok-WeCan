# src/feature_engineering.py
def add_features(df):
    """
    Menambahkan fitur baru jika diperlukan.
    Contoh: menambahkan kolom 'kehadiran_partisipasi' yang merupakan hasil perkalian
    antara 'kehadiran' dan 'partisipasi'.
    """
    df = df.copy()
    if 'kehadiran' in df.columns and 'partisipasi' in df.columns:
        df['kehadiran_partisipasi'] = df['kehadiran'] * df['partisipasi']
    return df
