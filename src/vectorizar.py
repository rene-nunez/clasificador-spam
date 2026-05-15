"""
Conversion de texto a vectores numericos con TF-IDF

Las maquinas no entienden texto, solo numeros.
TF-IDF convierte cada mensaje en un vector donde cada posicion 
representa una palabra y su valor indica que tan importante es.
"""

import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. Cargar datasets
train = pd.read_csv(os.path.join(BASE_DIR, "data", "train.csv"))
test = pd.read_csv(os.path.join(BASE_DIR, "data", "test.csv"))

# 2. Rellenar valores vacios que hayan quedado tras la limpieza
train["mensaje_limpio"] = train["mensaje_limpio"].fillna("")
test["mensaje_limpio"] = test["mensaje_limpio"].fillna("")

print(f"Train: {len(train)} mensajes")
print(f"Test: {len(test)} mensajes")

# 3. Crear y entrenar el vectorizador

# max_df=0.95 ignora palabras en mas del 95% de los mensajes
# min_df=2 ignora palabras que aparecen en menos de 2 mensajes
# ngram_range=(1,2) captura palabras individuales y pares de palabras
vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, ngram_range=(1, 2))

# fit_transform aprende el vocabulario Y transforma los textos de train
X_train = vectorizer.fit_transform(train["mensaje_limpio"])

# transform SOLO transforma test usando el vocabulario que ya aprendio
X_test = vectorizer.transform(test["mensaje_limpio"])

y_train = train["spam"]
y_test = test["spam"]

print(f"\nVocabulario aprendido: {len(vectorizer.get_feature_names_out())} palabras")
print(f"Train vectorizado: {X_train.shape}")
print(f"Test vectorizado: {X_test.shape}")

# 4. Guardar el vectorizador para usarlo después
models_dir = os.path.join(BASE_DIR, "models")
os.makedirs(models_dir, exist_ok=True)

joblib.dump(vectorizer, os.path.join(models_dir, "vectorizer.pkl"))
print(f"\nVectorizador guardado: models/vectorizer.pkl")