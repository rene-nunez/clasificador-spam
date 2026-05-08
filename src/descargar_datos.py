# Script para descargar el dataset de spam en español desde Hugging Face
# Dataset: tanaos/synthetic-spam-detection-dataset-spanish (15,016 mensajes)

from datasets import load_dataset
import pandas as pd

dataset = load_dataset("tanaos/synthetic-spam-detection-dataset-spanish")

# Convertir a DataFrame de pandas
df = pd.DataFrame(dataset["train"])

# Renombrar columnas
df.rename(columns={"text": "mensaje", "labels": "spam"}, inplace=True)

# 4. La columna 'spam' tiene 0 si no es spam, y 1 sí lo es. Agregamos una columna 'label'
df["label"] = df["spam"].map({0: "ham", 1: "spam"})

# 5. Guardar como CSV
df.to_csv("data/spam_dataset.csv", index=False)

print(f"Dataset guardado en data/spam_dataset.csv")
print(f"Total de mensajes: {len(df)}")
print(f"Spam: {df['spam'].sum()} | Ham: {len(df) - df['spam'].sum()}")
print(f"Columnas: {list(df.columns)}")
print("\nPrimeros 5 mensajes:")
print(df.head())