"""
Limpieza de texto del dataset de spam

Elimina duplicados, normaliza el texto (minusculas, puntuacion) 
y filtra stopwords en español usando nltk.
"""

import os
import re
import pandas as pd
import nltk

# Descargar stopwords de nltk si no estan instaladas
nltk.download("stopwords", quiet=True)
from nltk.corpus import stopwords

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta_csv = os.path.join(BASE_DIR, "data", "spam_dataset.csv")
df = pd.read_csv(ruta_csv)

print(f"Dataset cargado: {len(df)} mensajes")

# 1. Eliminar duplicados
antes = len(df)
df = df.drop_duplicates(subset=["mensaje"])
despues = len(df)
print(f"\nDuplicados eliminados: {antes - despues}")

# 2. Pasar a minusculas
df["mensaje"] = df["mensaje"].str.lower()

# 3. Eliminar signos de puntuación y caracteres especiales
df["mensaje_limpio"] = df["mensaje"].apply(
    # re.sub reemplaza todo lo que NO sea letra, numero o espacio por vacio
    lambda texto: re.sub(r"[^a-záéíóúüñA-ZÁÉÍÓÚÜÑ0-9\s]", "", texto)
)

# 4. Tokenizar y eliminar stopwords
stop_words = set(stopwords.words("spanish"))

def limpiar_texto(texto):
    tokens = texto.split()
    tokens = [t for t in tokens if t not in stop_words and len(t) > 1]
    return " ".join(tokens)

df["mensaje_limpio"] = df["mensaje_limpio"].apply(limpiar_texto)

# Guardar el nuevo dataset limpio
ruta_salida = os.path.join(BASE_DIR, "data", "spam_limpio.csv")
df.to_csv(ruta_salida, index=False)
print(f"\nDataset limpio guardado: data/spam_limpio.csv")
print(f"Mensajes finales: {len(df)}")

# 6. Mostrar comparación
print("\nComparacion antes/despues:")
for i in range(3):
    original = df["mensaje"].iloc[i]
    limpio = df["mensaje_limpio"].iloc[i]
    print(f"\nOriginal: {original}")
    print(f"Limpio: {limpio}")