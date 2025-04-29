# src/model.py
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

class Predictor:
    """
    Kelas untuk melatih dan melakukan prediksi menggunakan model machine learning.
    """
    def __init__(self):
        self.model = LogisticRegression()

    def train_model(self, X_train, y_train):
        """
        Melatih model menggunakan data train.
        """
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        """
        Menghasilkan prediksi berdasarkan data test.
        """
        return self.model.predict(X_test)

    def evaluate(self, X_test, y_test):
        """
        Mengevaluasi performa model menggunakan akurasi dan classification report.
        """
        y_pred = self.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, zero_division=0)
        return acc, report
