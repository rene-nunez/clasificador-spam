"""
Clasificar mensajes nuevos como spam o ham

Carga los modelos entrenados y permite probar mensajes
personalizados para ver si los detectan correctamente.
"""

import os
import re
import math
import joblib
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
stop_words = set(stopwords.words("spanish"))

# 1. Cargar modelos y vectorizador
vectorizer = joblib.load(os.path.join(BASE_DIR, "models", "vectorizer.pkl"))

modelos = {
    "Naive Bayes": joblib.load(os.path.join(BASE_DIR, "models", "naive_bayes.pkl")),
    "Regresion Logistica": joblib.load(os.path.join(BASE_DIR, "models", "regresion_logistica.pkl")),
    "SVM": joblib.load(os.path.join(BASE_DIR, "models", "svm.pkl")),
}

# 2. Limpiar el mensaje entrante
def limpiar_mensaje(texto):
    texto = texto.lower()
    texto = re.sub(r"[^a-záéíóúüñ0-9\s]", "", texto)
    tokens = texto.split()
    tokens = [t for t in tokens if t not in stop_words and len(t) > 1]
    return " ".join(tokens)

# 3. Clasificar con un modelo
def clasificar(texto, modelo):
    limpio = limpiar_mensaje(texto)
    vector = vectorizer.transform([limpio])
    pred = modelo.predict(vector)[0]

    if hasattr(modelo, "predict_proba"):
        prob = modelo.predict_proba(vector)[0]
        conf = prob[1] if pred == 1 else prob[0]
    else:
        d = modelo.decision_function(vector)[0]
        d = max(min(d, 100), -100)
        conf = 1 / (1 + math.exp(-d))

    return pred, conf

# 4. Modo interactivo
if __name__ == "__main__":
    nombres = list(modelos.keys())
    idx = 0

    print("Clasificador de spam")
    print(f"Modelo actual: {nombres[idx]} (cambia con: /modelo)")
    print("Escribe un mensaje para clasificarlo (o 'salir' para terminar)")
    print("")

    while True:
        entrada = input("> ")
        if entrada.lower() == "salir":
            break

        if entrada.startswith("/modelo"):
            idx = (idx + 1) % len(nombres)
            print(f"Modelo cambiado a: {nombres[idx]}")
            continue

        pred, conf = clasificar(entrada, modelos[nombres[idx]])
        etiqueta = "spam" if pred == 1 else "ham"
        print(f"{etiqueta} ({conf:.1%} de confianza)")
        print("")