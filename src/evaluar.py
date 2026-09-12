import os
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix, classification_report,
    precision_score, recall_score, f1_score
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTEBOOK_DIR = os.path.join(BASE_DIR, "notebook")

if __name__ == "__main__":
    os.makedirs(NOTEBOOK_DIR, exist_ok=True)

    test = pd.read_csv(os.path.join(BASE_DIR, "data", "test.csv"))
    test["mensaje_limpio"] = test["mensaje_limpio"].fillna("")

    vectorizer = joblib.load(os.path.join(BASE_DIR, "models", "vectorizer.pkl"))
    X_test = vectorizer.transform(test["mensaje_limpio"])
    y_test = test["spam"]

    modelos = {
        "Naive Bayes": "naive_bayes.pkl",
        "Regresion Logistica": "regresion_logistica.pkl",
        "SVM": "svm.pkl",
    }

    for nombre, archivo in modelos.items():
        print("-" * 30)
        print(f"{nombre}")
        print("-" * 30)

        modelo = joblib.load(os.path.join(BASE_DIR, "models", archivo))
        y_pred = modelo.predict(X_test)

        matriz = confusion_matrix(y_test, y_pred)
        print(f"\nMatriz de confusion:")
        print(f"              Prediccion")
        print(f"              ham  spam")
        print(f"Real  ham  {matriz[0,0]:>4} {matriz[0,1]:>4}")
        print(f"      spam {matriz[1,0]:>4} {matriz[1,1]:>4}")

        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        print(f"\nMetricas:")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1-Score: {f1:.4f}")

        plt.figure(figsize=(5, 4))
        sns.heatmap(matriz, annot=True, fmt="d", cmap="Blues", xticklabels=["ham", "spam"], yticklabels=["ham", "spam"])
        plt.title(f"Matriz de confusión: {nombre}")
        plt.ylabel("Real")
        plt.xlabel("Predicción")
        plt.tight_layout()
        archivo_matriz = os.path.join(NOTEBOOK_DIR, f"matriz_{nombre.lower().replace(' ', '_')}.png")
        plt.savefig(archivo_matriz)
        print(f"\nGráfico guardado: {archivo_matriz}")
        print("")

    print("-" * 30)
    print("Analisis de errores")
    print("-" * 30)

    predicciones = {}
    for nombre, archivo in modelos.items():
        modelo = joblib.load(os.path.join(BASE_DIR, "models", archivo))
        predicciones[nombre] = modelo.predict(X_test)

    print("\nComparacion de errores por modelo:")
    print(f"{'Modelo':25s} {'FP':>5s} {'FN':>5s} {'Total':>5s}")
    print("-" * 42)
    for nombre in modelos:
        y_pred = predicciones[nombre]
        fp = ((y_test == 0) & (y_pred == 1)).sum()
        fn = ((y_test == 1) & (y_pred == 0)).sum()
        print(f"{nombre:25s} {fp:5d} {fn:5d} {fp+fn:5d}")

    test["fp_todos"] = (
        (y_test == 0)
        & (predicciones["Naive Bayes"] == 1)
        & (predicciones["Regresion Logistica"] == 1)
        & (predicciones["SVM"] == 1)
    )

    test["fn_todos"] = (
        (y_test == 1)
        & (predicciones["Naive Bayes"] == 0)
        & (predicciones["Regresion Logistica"] == 0)
        & (predicciones["SVM"] == 0)
    )

    print("")
    print(f"Casos donde todos los modelos fallaron:")
    print(f"Falsos positivos (ham que todos dijeron spam): {test['fp_todos'].sum()}")
    print(f"Falsos negativos (spam que todos dijeron ham): {test['fn_todos'].sum()}")

    if test['fp_todos'].sum() > 0 or test['fn_todos'].sum() > 0:
        print(f"\nEjemplos mas dificiles:")
        for _, mensaje in test[test["fp_todos"] | test["fn_todos"]].head(6).iterrows():
            tipo = "FP" if mensaje["fp_todos"] else "FN"
            print(f"  [{tipo}] {mensaje['mensaje_limpio'][:80]}")
