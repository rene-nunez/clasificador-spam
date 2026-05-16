"""
Clasificar mensajes nuevos como spam o ham

Carga el modelo entrenado y permite probar mensajes
personalizados para ver si los detecta correctamente.
"""

import os
import re
import joblib
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. Cargar modelo y vectorizador
modelo = joblib.load(os.path.join(BASE_DIR, "models", "regresion_logistica.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "models", "vectorizer.pkl"))

stop_words = set(stopwords.words("spanish"))

# 2. Limpiar el mensaje entrante
def limpiar_mensaje(texto):
    texto = texto.lower()
    texto = re.sub(r"[^a-záéíóúüñ0-9\s]", "", texto)
    tokens = texto.split()
    tokens = [t for t in tokens if t not in stop_words and len(t) > 1]
    return " ".join(tokens)

# 3. Vectorizar y predecir el mensaje
def clasificar(texto):
    limpio = limpiar_mensaje(texto)
    vector = vectorizer.transform([limpio])
    prediccion = modelo.predict(vector)[0]
    probabilidad = modelo.predict_proba(vector)[0]
    confianza = probabilidad[1] if prediccion == 1 else probabilidad[0]
    return prediccion, confianza

# 4. Modo interactivo
print("Clasificador de spam")
print("Escribe un mensaje para clasificarlo (o 'salir' para terminar)")
print("")

while True:
    mensaje = input("> ")
    if mensaje.lower() == "salir":
        break

    pred, conf = clasificar(mensaje)
    etiqueta = "spam" if pred == 1 else "ham"
    print(f"{etiqueta} ({conf:.1%} de confianza)")
    print("")