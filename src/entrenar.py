"""
Entrenamiento de modelos

Entrena Naive Bayes Multinomial, Regresion Logistica y SVM
con los datos vectorizados, guarda los modelos entrenados.
"""

import os
import pandas as pd
import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. Cargar datasets
train = pd.read_csv(os.path.join(BASE_DIR, "data", "train.csv"))
test = pd.read_csv(os.path.join(BASE_DIR, "data", "test.csv"))

train["mensaje_limpio"] = train["mensaje_limpio"].fillna("")
test["mensaje_limpio"] = test["mensaje_limpio"].fillna("")

# 2. Cargar vectorizador y transformar datos
vectorizer = joblib.load(os.path.join(BASE_DIR, "models", "vectorizer.pkl"))
X_train = vectorizer.transform(train["mensaje_limpio"])
X_test = vectorizer.transform(test["mensaje_limpio"])
y_train = train["spam"]
y_test = test["spam"]

print(f"Datos cargados: {X_train.shape[0]} train, {X_test.shape[0]} test")

# 3. Entrenar modelos
modelos = {
    "Naive Bayes": MultinomialNB(),
    "Regresion Logistica": LogisticRegression(max_iter=1000, random_state=42),
    "SVM": LinearSVC(random_state=42),
}

resultados = []

for nombre, modelo in modelos.items():
    print(f"\nEntrenando {nombre}...")
    modelo.fit(X_train, y_train)
    precision = modelo.score(X_test, y_test)
    resultados.append((nombre, precision))
    print(f"Exactitud en test: {precision:.4f}")

    # Guardar modelo
    archivo = f"{nombre.lower().replace(' ', '_')}.pkl"
    joblib.dump(modelo, os.path.join(BASE_DIR, "models", archivo))
    print(f"Modelo guardado: models/{archivo}")

# 4. Resumen
print("\n" + "-" * 30)
print("Exactitud en test")
print("-" * 30)
for nombre, precision in resultados:
    print(f"{nombre:22s}: {precision:.4f}")