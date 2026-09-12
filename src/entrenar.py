# Entrena Naive Bayes Multinomial, Regresion Logistica y SVM

import os
import pandas as pd
import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    train = pd.read_csv(os.path.join(BASE_DIR, "data", "train.csv"))
    test = pd.read_csv(os.path.join(BASE_DIR, "data", "test.csv"))

    train["mensaje_limpio"] = train["mensaje_limpio"].fillna("")
    test["mensaje_limpio"] = test["mensaje_limpio"].fillna("")

    vectorizer = joblib.load(os.path.join(BASE_DIR, "models", "vectorizer.pkl"))
    X_train = vectorizer.transform(train["mensaje_limpio"])
    X_test = vectorizer.transform(test["mensaje_limpio"])
    y_train = train["spam"]
    y_test = test["spam"]

    print(f"Datos cargados: {X_train.shape[0]} train, {X_test.shape[0]} test")

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

        archivo = f"{nombre.lower().replace(' ', '_')}.pkl"
        joblib.dump(modelo, os.path.join(BASE_DIR, "models", archivo))
        print(f"Modelo guardado: models/{archivo}")

    print("\n" + "-" * 30)
    print("Exactitud en test")
    print("-" * 30)
    for nombre, precision in resultados:
        print(f"{nombre:22s}: {precision:.4f}")
