import os
import joblib
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

stop_words = set(stopwords.words("spanish"))

vectorizer = joblib.load(os.path.join(BASE_DIR, "models", "vectorizer.pkl"))

modelos = {
    "Regresión Logística": joblib.load(os.path.join(BASE_DIR, "models", "regresion_logistica.pkl")),
    "Naive Bayes": joblib.load(os.path.join(BASE_DIR, "models", "naive_bayes.pkl")),
    "SVM": joblib.load(os.path.join(BASE_DIR, "models", "svm.pkl")),
}
