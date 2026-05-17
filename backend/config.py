"""
Configuración global del backend

Carga los modelos ML entrenados, el vectorizador TF-IDF
y las stopwords en español desde el disco.
"""

import os
import joblib
import nltk
from nltk.corpus import stopwords

# Descarga silenciosa de stopwords en español
nltk.download("stopwords", quiet=True)

# Obtiene la ruta raíz del proyecto, BASE_DIR apunta a la raíz
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Conjunto de palabras vacías (stopwords) en español (ej. "el", "la", "de", etc.)
stop_words = set(stopwords.words("spanish"))

# Vectorizador entrenado
# Convierte texto en vectores numéricos para que los modelos de ML puedan procesarlo
vectorizer = joblib.load(os.path.join(BASE_DIR, "models", "vectorizer.pkl"))

# Carga de modelos ML con joblib
modelos = {
    "Regresión Logística": joblib.load(os.path.join(BASE_DIR, "models", "regresion_logistica.pkl")),
    "Naive Bayes": joblib.load(os.path.join(BASE_DIR, "models", "naive_bayes.pkl")),
    "SVM": joblib.load(os.path.join(BASE_DIR, "models", "svm.pkl")),
}