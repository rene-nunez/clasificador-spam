"""
Division del dataset en entrenamiento (80%) y prueba (20%)

El modelo se entrena con train y se evalua con test 
para medir su rendimiento en datos que nunca ha visto.
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta_csv = os.path.join(BASE_DIR, "data", "spam_limpio.csv")
df = pd.read_csv(ruta_csv)

print(f"Dataset cargado: {len(df)} mensajes")

# Dividir el DataFrame directamente en train (80%) y test (20%)
# stratify=df["spam"] mantiene la misma proporción spam/ham en ambos
# random_state=42 fija la semilla para que sea reproducible
train, test = train_test_split(
    df, test_size=0.2, random_state=42, stratify=df["spam"]
)

# Guardar
train.to_csv(os.path.join(BASE_DIR, "data", "train.csv"), index=False)
test.to_csv(os.path.join(BASE_DIR, "data", "test.csv"), index=False)

print(f"\nTrain: {len(train)} mensajes")
print(f"spam: {train['spam'].sum()}, ham: {len(train) - train['spam'].sum()}")
print("")
print(f"Test: {len(test)} mensajes")
print(f"spam: {test['spam'].sum()}, ham: {len(test) - test['spam'].sum()}")
print(f"\nProporcion spam/ham mantenida en ambos")