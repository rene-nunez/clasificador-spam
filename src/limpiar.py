import os
import re
import pandas as pd
import nltk

nltk.download("stopwords", quiet=True)
from nltk.corpus import stopwords

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    ruta_csv = os.path.join(BASE_DIR, "data", "spam_dataset.csv")
    df = pd.read_csv(ruta_csv)

    print(f"Dataset cargado: {len(df)} mensajes")

    antes = len(df)
    df = df.drop_duplicates(subset=["mensaje"])
    despues = len(df)
    print(f"\nDuplicados eliminados: {antes - despues}")

    df["mensaje"] = df["mensaje"].str.lower()

    df["mensaje_limpio"] = df["mensaje"].apply(
        lambda texto: re.sub(r"[^a-záéíóúüñ0-9\s]", "", texto)
    )

    stop_words = set(stopwords.words("spanish"))

    def limpiar_texto(texto):
        tokens = texto.split()
        tokens = [t for t in tokens if t not in stop_words and len(t) > 1]
        return " ".join(tokens)

    df["mensaje_limpio"] = df["mensaje_limpio"].apply(limpiar_texto)

    ruta_salida = os.path.join(BASE_DIR, "data", "spam_limpio.csv")
    df.to_csv(ruta_salida, index=False)
    print(f"\nDataset limpio guardado: data/spam_limpio.csv")

    print("\nComparacion antes/despues:")
    for i in range(3):
        original = df["mensaje"].iloc[i]
        limpio = df["mensaje_limpio"].iloc[i]
        print(f"\nOriginal: {original}")
        print(f"Limpio: {limpio}")
